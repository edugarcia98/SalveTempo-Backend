from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import *
from .serializers import *

from rest_framework import mixins, generics, status, filters, views
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#Localização
#==========================================================================================================
class PaisList(generics.ListCreateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class EstadoList(generics.ListCreateAPIView):
    search_fields = ['pais__nome', ]
    filter_backends = (filters.SearchFilter, )
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class CidadeList(generics.ListCreateAPIView):
    search_fields = ['estado__sigla', ]
    filter_backends = (filters.SearchFilter, )
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CidadeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class EnderecoList(generics.ListCreateAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class EnderecoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class UnidadeSaudeList(generics.ListCreateAPIView):
    queryset = UnidadeSaude.objects.all()
    serializer_class = UnidadeSaudeSerializer

class UnidadeSaudeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnidadeSaude.objects.all()
    serializer_class = UnidadeSaudeSerializer

#Doenças
#==========================================================================================================

class DoencaList(generics.ListCreateAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer

class DoencaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doenca.objects.all()
    serializer_class = DoencaSerializer

class EspecializacaoList(generics.ListCreateAPIView):
    queryset = Especializacao.objects.all()
    serializer_class = EspecializacaoSerializer

class EspecializacaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Especializacao.objects.all()
    serializer_class = EspecializacaoSerializer

class EspecializacaoDoencaList(generics.ListCreateAPIView):
    queryset = EspecializacaoDoenca.objects.all()
    serializer_class = EspecializacaoDoencaSerializer

class EspecializacaoDoencaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EspecializacaoDoenca.objects.all()
    serializer_class = EspecializacaoDoencaSerializer

#Usuários
#==========================================================================================================

class PacienteList(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class PacienteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class MedicoList(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class MedicoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class MedicoUnidadeSaudeList(generics.ListCreateAPIView):
    queryset = MedicoUnidadeSaude.objects.all()
    serializer_class = MedicoUnidadeSaudeSerializer

class MedicoUnidadeSaudeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicoUnidadeSaude.objects.all()
    serializer_class = MedicoUnidadeSaudeSerializer

#Consulta
#==========================================================================================================

class SintomaList(generics.ListCreateAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class SintomaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer

class TestView(views.APIView):

    def get(self, request):
        data = []
        for x in range(0, 100):
            nums = {"a": x, "b": x}
            data.append(nums)
        results = TestSerializer(data, many=True).data
        return Response(results)