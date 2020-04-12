import pandas as pd
from app.models import *

#Cadastrando doenças

Doenca.objects.all().delete()

doencas = pd.read_csv('data/data_doencas.csv', sep=';', index_col=None, encoding='latin-1')

for i in doencas['prognostico']:
    nome = i
    
    obj, created = Doenca.objects.get_or_create(nome=nome)
    if created:
        obj.save()
        print('Salvou: ' + str(obj))