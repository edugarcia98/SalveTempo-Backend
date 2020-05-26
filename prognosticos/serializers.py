from .models import *
from rest_framework import serializers

class ShowSintomaSerializer(serializers.Serializer):
    nomecsv = serializers.CharField(max_length=100)
    nome = serializers.CharField(max_length=150)