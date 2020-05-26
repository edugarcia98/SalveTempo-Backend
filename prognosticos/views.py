from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import *
from app.models import Sintoma
from .serializers import *

from rest_framework import mixins, generics, status, filters, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import pandas as pd
import numpy as np

#Métodos
def symptom_counter(prognosticos, symptoms, used_symptoms):
    symptom_counter = []
    sintomas = used_symptoms.keys()

    for key in used_symptoms.keys():
        answer = int(used_symptoms[key])
        if answer in (0, 1):
            prognosticos = prognosticos.loc[prognosticos[key] == answer]

    for s in symptoms:
        if not s in sintomas:
            s_dict = {'symptom': s, 'occurrences': len(prognosticos[prognosticos[s] == 1])}
            symptom_counter.append(s_dict)

    symptom_counter_ordered = sorted(symptom_counter, key = lambda i: i['occurrences'], reverse=True)
    return symptom_counter_ordered

def doenca_counter(prognosticos, used_symptoms):
    for key in used_symptoms.keys():
        answer = int(used_symptoms[key])
        if answer in (0, 1):
            prognosticos = prognosticos.loc[prognosticos[key] == answer]
    doencas = prognosticos.prognostico.unique()
    return len(doencas)

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
        
        data = [{"nomecsv": sintoma, "nome": Sintoma.objects.get(nomecsv=sintoma).nome}]
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