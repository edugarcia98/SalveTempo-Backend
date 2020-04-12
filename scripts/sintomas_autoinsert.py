import pandas as pd
from app.models import *

#Cadastrando sintomas

Sintoma.objects.all().delete()

sintomas = pd.read_csv('data/data_sintomas.csv', sep=';', index_col=None, encoding='latin-1')

for i in range(len(sintomas)):
    nomecsv = sintomas['Sintoma_CSV'][i]
    nome = sintomas['Sintoma_Descricao'][i]

    obj, created = Sintoma.objects.get_or_create(nomecsv=nomecsv, nome=nome)
    if created:
        obj.save()
        print('Salvou: ' + str(obj))