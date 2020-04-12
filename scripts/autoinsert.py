import pandas as pd
from app.models import *

#Cadastrando País

Pais.objects.all().delete()

pais = Pais(nome='Brasil')
pais.save()

#Cadastrando Estados
Estado.objects.all().delete()

estados = pd.read_csv('data/estados.csv', sep=',', index_col=None)

for i in range(estados.shape[0]):
    pais = Pais.objects.get(nome=estados['COD_PAIS'][i])
    sigla = estados['SIGLA'][i]
    nome = estados['NOME'][i]

    estado = Estado(pais=pais, sigla=sigla, nome=nome)
    estado.save()
    print('Salvou: ' + str(estado))

#Cadastrando Cidades
Cidade.objects.all().delete()

cidades = pd.read_csv('data/cidades.csv', sep=';', index_col=None)

for i in range(cidades.shape[0]):
    estado = Estado.objects.get(sigla=cidades['UF'][i].strip())
    nome = cidades['Nome do Município'][i].strip()
    latitude = cidades['Latitude'][i]
    longitude = cidades['Longitude'][i]

    cidade = Cidade(estado=estado, nome=nome, latitude=latitude, longitude=longitude)
    cidade.save()
    print('Salvou: ' + str(cidade))