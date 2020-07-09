from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Endereco)
admin.site.register(UnidadeSaude)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(MedicoUnidadeSaude)
admin.site.register(AdminUnidadeSaude)
admin.site.register(Doenca)
admin.site.register(Especializacao)
admin.site.register(EspecializacaoDoenca)
admin.site.register(Sintoma)
admin.site.register(Consulta)
admin.site.register(ConsultaSintoma)
admin.site.register(Prognostico)