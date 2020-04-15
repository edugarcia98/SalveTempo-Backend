from django.db import models
from SalveTempo import settings

# Create your models here.

#Localização
#==========================================================================================================
class Pais(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ('nome',)
        verbose_name = ("País")
        verbose_name_plural = ("Países")

class Estado(models.Model):
    pais = models.ForeignKey(Pais, verbose_name="País", on_delete=models.CASCADE)
    sigla = models.CharField(max_length=2, verbose_name="Sigla")
    nome = models.CharField(max_length=50, verbose_name="Nome")

    def __str__(self):
        return self.sigla
    
    class Meta:
        ordering = ('sigla',)
        verbose_name = ("Estado")
        verbose_name_plural = ("Estados")

class Cidade(models.Model):
    estado = models.ForeignKey(Estado, verbose_name="Estado", on_delete=models.CASCADE)
    nome = models.CharField(max_length=75, verbose_name="Nome")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    def __str__(self):
        return self.nome + ', ' + self.estado.sigla
    
    class Meta:
        ordering = ('nome',)
        verbose_name = ("Cidade")
        verbose_name_plural = ("Cidades")

class Endereco(models.Model):
    cidade = models.ForeignKey(Cidade, verbose_name="Cidade", on_delete=models.CASCADE)
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    logradouro = models.CharField(max_length=200, verbose_name="Logradouro")
    numero = models.CharField(max_length=8, verbose_name="Número")
    complemento = models.CharField(max_length=50, blank=True, verbose_name="Complemento")

    def __str__(self):
        final_str = self.logradouro + ', ' + self.numero

        if not self.complemento == '':
            final_str += ', ' + self.complemento
        
        final_str += ' - ' + self.bairro + ', ' + self.cidade.nome + ' - ' + self.cidade.estado.sigla
        return final_str

    class Meta:
        ordering = ('logradouro', 'bairro',)
        verbose_name = ("Endereço")
        verbose_name_plural = ("Endereços")

class UnidadeSaude(models.Model):
    TIPO_UNIDADE_SAUDE = (
        ('PS', 'Posto de Saúde'),
        ('UBS', 'Centro de Saúde/Unidade Básica de Saúde'),
        ('PC', 'Policlínica'),
        ('HG', 'Hospital Geral'),
        ('HE', 'Hospital Especializado'),
        ('UM', 'Unidade Mista'),
        ('PSG', 'Pronto Socorro Geral'),
        ('PSE', 'Pronto Socorro Especializado'),
        ('CI', 'Consultório Isolado'),
        ('UMF', 'Unidade Móvel Fluvial'),
        ('CE', 'Clínica Especializada/Amb. Especializado'),
        ('USADT', 'Unidade de Serviço de Apoio a Diagnose e Terapia'),
        ('UMT', 'Unidade Móvel Terrestre'),
        ('UMNPAUE', 'Unidade Móvel de Nível Pré-hospitalar na Área de Urgência e Emergência'),
        ('HDI', 'Hospital/Dia-Isolado'),
    )

    nome = models.CharField(max_length=150, verbose_name="Nome")
    endereco = models.ForeignKey(Endereco, verbose_name="Endereço", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_UNIDADE_SAUDE, verbose_name="Tipo")
    
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = ("Unidade de Saúde")
        verbose_name_plural = ("Unidades de Saúde")

#Doenças
#==========================================================================================================
class Doenca(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = ("Doença")
        verbose_name_plural = ("Doenças")

class Especializacao(models.Model):
    nome = models.CharField(max_length=70, verbose_name="Nome")
    doencas = models.ManyToManyField(Doenca, verbose_name="Doenças", through='EspecializacaoDoenca')
    
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = ("Especialização")
        verbose_name_plural = ("Especializações")

class EspecializacaoDoenca(models.Model):
    especializacao = models.ForeignKey(Especializacao, verbose_name="Especialização", on_delete=models.CASCADE)
    doenca = models.ForeignKey(Doenca, verbose_name="Doença", on_delete=models.CASCADE)

    def __str__(self):
        return self.especializacao.nome + ' - ' + self.doenca.nome

    class Meta:
        verbose_name = ("Especialização - Doença")
        verbose_name_plural = ("Especializações - Doenças")

#Usuários
#==========================================================================================================
class Usuario(models.Model):
    USUARIO_SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    nome = models.CharField(max_length=50, verbose_name="Nome")
    sexo = models.CharField(max_length=1, choices=USUARIO_SEXO, verbose_name="Sexo")
    dataNasc = models.DateField(verbose_name="Data de Nascimento")
    #email = models.EmailField(verbose_name="E-mail")
    #senha = models.CharField(max_length=20, verbose_name="Senha")

    class Meta:
        abstract = True

class Paciente(Usuario):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paciente')

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ('nome',)
        verbose_name = ("Paciente")
        verbose_name_plural = ("Pacientes")

class Medico(Usuario):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medico')
    unidadesSaude = models.ManyToManyField(UnidadeSaude, verbose_name="Unidades de Saúde", through='MedicoUnidadeSaude')
    especializacao = models.ForeignKey(Especializacao, verbose_name="Especialização", on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = ("Médico")
        verbose_name_plural = ("Médicos")

class MedicoUnidadeSaude(models.Model):
    medico = models.ForeignKey(Medico, verbose_name="Médico", on_delete=models.CASCADE)
    unidadeSaude = models.ForeignKey(UnidadeSaude, verbose_name="Unidade de Saúde", on_delete=models.CASCADE)
    diaPeriodoTrabalho = models.CharField(max_length=500, verbose_name="Dias e Período de Trabalho")

    def __str__(self):
        return self.medico.nome + ' - ' + self.unidadeSaude.nome
    
    class Meta:
        verbose_name = ("Médico - Unidade de Saúde")
        verbose_name_plural = ("Médicos - Unidades de Saúde")

#Consulta
#==========================================================================================================
class Sintoma(models.Model):
    nomecsv = models.CharField(max_length=100, verbose_name="Nome CSV")
    nome = models.CharField(max_length=150, verbose_name="Nome")

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = ("Sintoma")
        verbose_name_plural = ("Sintomas")

class Consulta(models.Model):
    PERIODO = (
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('N', 'Noite'),
    )

    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    unidadeSaude = models.ForeignKey(UnidadeSaude, verbose_name="Unidade de Saúde", on_delete=models.CASCADE)
    #anamnese: pesquisar todos os campos
    sintomas = models.ManyToManyField(Sintoma, verbose_name="Sintomas", through='ConsultaSintoma')
    medico = models.ForeignKey(Medico, verbose_name="Médico", on_delete=models.CASCADE)
    data = models.DateField(verbose_name="Data da Consulta")
    periodo = models.CharField(max_length=1, choices=PERIODO, verbose_name="Período")
    prognosticos = models.ManyToManyField(Doenca, verbose_name='Prognóstico', through='Prognostico')
    percentual_assertividade_prognostico = models.FloatField(verbose_name="Percentual de Assertividade do Prognóstico")

    def __str__(self):
        return 'Consulta do paciente ' + self.paciente.nome + ' com o Doutor ' + self.medico.nome + ' no dia ' + str(self.data) + ' no período da ' + self.periodo

    class Meta:
        verbose_name = ("Consulta")
        verbose_name_plural = ("Consultas")

class ConsultaSintoma(models.Model):
    consulta = models.ForeignKey(Consulta, verbose_name="Consulta", on_delete=models.CASCADE)
    sintoma = models.ForeignKey(Sintoma, verbose_name="Sintoma", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.consulta) + ' - ' + self.sintoma.nome

    class Meta:
        verbose_name = ("Consulta - Sintoma")
        verbose_name_plural = ("Consultas - Sintomas")

class Prognostico(models.Model):
    consulta = models.ForeignKey(Consulta, verbose_name="Consulta", on_delete=models.CASCADE)
    doenca = models.ForeignKey(Doenca, verbose_name="Doença", on_delete=models.CASCADE)
    percentual = models.FloatField(verbose_name="Percentual")

    def __str__(self):
        return str(self.consulta) + ' - ' + self.doenca.nome + ' - ' + str(self.percentual) + '%'

    class Meta:
        verbose_name = ("Prognóstico")
        verbose_name_plural = ("Prognósticos")