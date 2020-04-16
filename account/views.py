from django.shortcuts import render

from .models import *
from .serializers import *

from rest_framework import mixins, generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class UserList(generics.ListCreateAPIView):
    #Verificar se é possível e/ou necessário bloquear GET em User
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer