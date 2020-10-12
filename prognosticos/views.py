from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import connection

from .models import *
from app.models import Sintoma, Doenca
from .serializers import *
from app.serializers import SintomaSerializer

from rest_framework import mixins, generics, status, filters, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import pandas as pd
import numpy as np

from unidecode import unidecode

#Métodos
def hasValidData(data):
    for key in data.keys():
        if data[key] in ('0', '1'):
            return True
    return False

def symptom_counter(prognosticos, symptoms, used_symptoms):
    symptom_counter = []
    sintomas = used_symptoms.keys()

    for s in symptoms:
        if not s in sintomas:
            s_dict = {'symptom': s, 'occurrences': len(prognosticos[prognosticos[s] == 1])}
            symptom_counter.append(s_dict)

    symptom_counter_ordered = sorted(symptom_counter, key = lambda i: i['occurrences'], reverse=True)
    return symptom_counter_ordered

def doenca_counter(prognosticos, used_symptoms):
    doencas = prognosticos.prognostico.unique()
    return len(doencas)

def resultados_prognosticos(prognosticos, used_symptoms):
    doencas = prognosticos.prognostico.unique()

    progs = []

    for d in doencas:
        pct = (len(prognosticos[prognosticos['prognostico'] == d])/len(prognosticos)) * 100
        pct = round(pct, 2)

        doenca_bd = Doenca.objects.get(nome=d)

        prog_dict = {'id': doenca_bd.id, 'doenca': d, 'porcentagem': pct}
        progs.append(prog_dict)
    
    return sorted(progs, key = lambda i: i['porcentagem'], reverse=True)

def saveNewSintomaToDb(data):
    sql_command = 'ALTER TABLE prognosticos_prognosticodata ADD COLUMN ' + \
        data['nomecsv'] + ' INTEGER DEFAULT 0;'
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
        return True
    except:
        return False

def saveNewResultadoToDb(data):
    fields = ''
    values = ''

    for sintoma in Sintoma.objects.all():
        sintoma_csv = sintoma.nomecsv
        fields += sintoma_csv + ', '
        values += str(data[sintoma_csv]) + ', ' if sintoma_csv in data.keys() else '0' + ', '
    
    fields += 'prognostico'
    values += '\'' + data['prognostico'] + '\''

    sql_command = 'INSERT INTO prognosticos_prognosticodata (' + fields + \
        ') VALUES (' + values + ');'

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
        return True
    except:
        return False

def init_dataframe(data):
    with connection.cursor() as cursor:
        sql_query = 'SELECT '
        fields = ''
        fields_list = []

        for sintoma in Sintoma.objects.all():
            fields += sintoma.nomecsv + ', '
            fields_list.append(sintoma.nomecsv)
        
        fields += 'prognostico'
        fields_list.append('prognostico')

        sql_query += fields + ' FROM prognosticos_prognosticodata'
        
        if not hasValidData(data):
            sql_query += ';'
        else:
            sql_query += ' WHERE '
            
            for key in data.keys():
                if data[key] in ('0', '1'):
                    sql_query += ' ' + key + ' = ' + str(data[key]) + ' AND'
            sql_query = sql_query.rsplit(' ', 1)[0] + ';'

        cursor.execute(sql_query)
        df = pd.DataFrame(cursor.fetchall(), columns=fields_list)

        symptoms = df.iloc[:,:-1].columns.values.tolist()

    return df, symptoms

# Create your views here.
class StartConsulta(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        return Response(request.data, status=status.HTTP_201_CREATED)

class ShowSintomaView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        used_symptoms = request.data
        prognosticos, symptoms = init_dataframe(used_symptoms)
        
        sintomas = symptom_counter(prognosticos, symptoms, used_symptoms)
        sintoma = sintomas[0]['symptom']
        
        sintoma_bd = Sintoma.objects.get(nomecsv=sintoma)

        data = [{"id": sintoma_bd.id, "nomecsv": sintoma, "nome": sintoma_bd.nome}]
        results = ShowSintomaSerializer(data, many=True).data
        return Response(results)

class AnswerSintomaView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        used_symptoms = request.data
        prognosticos, symptoms = init_dataframe(used_symptoms)
        valido = True

        n_doencas = doenca_counter(prognosticos, used_symptoms)

        if (len(used_symptoms) >= len(symptoms)) and (n_doencas > 3):
            valido = False

        data = [{"counter_doencas": n_doencas, "valido": valido}]
        return Response(data, status=status.HTTP_201_CREATED)

class ReturnPrognosticosView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        used_symptoms = request.data
        prognosticos, symptoms = init_dataframe(used_symptoms)

        data = resultados_prognosticos(prognosticos, used_symptoms)
        return Response(data, status=status.HTTP_201_CREATED)

class SavePrognosticoToDb(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        if data['prognostico'] == '':
            response = {'error': 'O campo "prognostico" não pode ser vazio.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if saveNewResultadoToDb(data):
            response = {'success': 'Resultado de consulta salvo com sucesso.'}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {'error': 'Ocorreu algo errado ao salvar o resultado.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class NewSintomaFieldToDb(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        data['nomecsv'] = unidecode(data['nome'].replace(' ', '_').lower())
        
        serializer = SintomaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            #Salvando o sintoma na tabela de sintomas
            if saveNewSintomaToDb(data):
                #response = {'success': 'Campo de sintoma salvo com sucesso.'}
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            response = {'error': 'Ocorreu algo errado ao salvar o sintoma no banco de prognósticos.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)