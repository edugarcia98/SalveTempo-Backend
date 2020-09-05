from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import *
from app.models import Sintoma, Doenca
from .serializers import *

from rest_framework import mixins, generics, status, filters, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import pandas as pd
import numpy as np

#Métodos
def process_prognosticos_data(prognosticos, used_symptoms):
    for key in used_symptoms.keys():
        answer = int(used_symptoms[key])
        if answer in (0, 1):
            prognosticos = prognosticos.loc[prognosticos[key] == answer]
    
    return prognosticos

def symptom_counter(prognosticos, symptoms, used_symptoms):
    symptom_counter = []
    sintomas = used_symptoms.keys()

    prognosticos = process_prognosticos_data(prognosticos, used_symptoms)

    for s in symptoms:
        if not s in sintomas:
            s_dict = {'symptom': s, 'occurrences': len(prognosticos[prognosticos[s] == 1])}
            symptom_counter.append(s_dict)

    symptom_counter_ordered = sorted(symptom_counter, key = lambda i: i['occurrences'], reverse=True)
    return symptom_counter_ordered

def doenca_counter(prognosticos, used_symptoms):
    prognosticos = process_prognosticos_data(prognosticos, used_symptoms)
    doencas = prognosticos.prognostico.unique()
    return len(doencas)

def resultados_prognosticos(prognosticos, used_symptoms):
    prognosticos = process_prognosticos_data(prognosticos, used_symptoms)
    doencas = prognosticos.prognostico.unique()

    progs = []

    for d in doencas:
        pct = (len(prognosticos[prognosticos['prognostico'] == d])/len(prognosticos)) * 100
        pct = round(pct, 2)

        doenca_bd = Doenca.objects.get(nome=d)

        prog_dict = {'id': doenca_bd.id, 'doenca': d, 'porcentagem': pct}
        progs.append(prog_dict)
    
    return sorted(progs, key = lambda i: i['porcentagem'], reverse=True)

#Iniciando o DataFrame
df = pd.DataFrame(PrognosticoData.objects.values_list())
field_names = PrognosticoData._meta.get_fields()

index = {}
index_n = 0
for i in field_names:
    index[index_n] = i.name
    index_n += 1

df.rename(columns=index, inplace=True)
prognosticos = df.copy()
prognosticos = prognosticos.drop('id', axis=1)

symptoms = df.iloc[:,:-1].columns.values.tolist()
id_col = symptoms[0]
symptoms.remove(id_col)

# Create your views here.
class StartConsulta(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        return Response(request.data, status=status.HTTP_201_CREATED)

class ShowSintomaView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        used_symptoms = request.data
        
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

        data = resultados_prognosticos(prognosticos, used_symptoms)
        return Response(data, status=status.HTTP_201_CREATED)

class SavePrognosticoToDb(views.APIView):
    #permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        keys = data.keys()
        
        p = PrognosticoData()

        for key in keys:
            setattr(p, key, data[key])
        print(p.casca_ferida_amarela)
        print(p.febre_alta)
        print(p.comichao)
        print(p.prognostico)

        p.save()
        
        return Response({'ok': 'ok'});