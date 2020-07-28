from .models import *
from rest_framework import serializers

class ShowSintomaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nomecsv = serializers.CharField(max_length=100)
    nome = serializers.CharField(max_length=150)