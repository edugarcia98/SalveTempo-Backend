from .models import *
from rest_framework import serializers

#Localização
#==========================================================================================================
class PaisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pais
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):

    pais = PaisSerializer(read_only=True)

    pais_id = serializers.PrimaryKeyRelatedField(
        queryset=Pais.objects.all(), source='pais', write_only=True
    )

    class Meta:
        model = Estado
        #depth = 1
        fields = '__all__'

class CidadeSerializer(serializers.ModelSerializer):

    estado = EstadoSerializer(read_only=True)

    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=Estado.objects.all(), source='estado', write_only=True
    )

    class Meta:
        model = Cidade
        depth = 1
        fields = '__all__'

class EnderecoSerializer(serializers.ModelSerializer):

    cidade = CidadeSerializer(read_only=True)

    cidade_id = serializers.PrimaryKeyRelatedField(
        queryset=Cidade.objects.all(), source='cidade', write_only=True
    )

    class Meta:
        model = Endereco
        depth = 1
        fields = '__all__'

class UnidadeSaudeSerializer(serializers.ModelSerializer):

    endereco = EnderecoSerializer(read_only=True)

    endereco_id = serializers.PrimaryKeyRelatedField(
        queryset=Endereco.objects.all(), source='endereco', write_only=True
    )

    class Meta:
        model = UnidadeSaude
        depth = 1
        fields = '__all__'

#Doenças
#==========================================================================================================

class DoencaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doenca
        fields = '__all__'

class EspecializacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especializacao
        depth = 1
        fields = '__all__'

class EspecializacaoDoencaSerializer(serializers.ModelSerializer):

    especializacao = EspecializacaoSerializer(read_only=True)

    especializacao_id = serializers.PrimaryKeyRelatedField(
        queryset=Especializacao.objects.all(), source='especializacao', write_only=True
    )

    doenca = DoencaSerializer(read_only=True)

    doenca_id = serializers.PrimaryKeyRelatedField(
        queryset=Doenca.objects.all(), source='doenca', write_only=True
    )

    class Meta:
        model = EspecializacaoDoenca
        fields = '__all__'


#Consulta
#==========================================================================================================

class SintomaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sintoma
        fields = '__all__'