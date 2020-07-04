from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import *
from .serializers import *

from rest_framework import mixins, generics, status, filters, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

class UserList(generics.ListCreateAPIView):
    #Verificar se é possível e/ou necessário bloquear GET em User
    search_fields = ['=email', ]
    filter_backends = (filters.SearchFilter, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def complete_view(request):
    return Response("E-mail está ativado.")
