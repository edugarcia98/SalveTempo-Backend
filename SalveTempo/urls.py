"""SalveTempo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

#from allauth.account.views import ConfirmEmailView
#from allauth.account.views import confirm_email as allauthemailconfirmation
#from rest_auth.registration.views import VerifyEmailView
from allauth.account.views import confirm_email

from app import views
from accountuser import views as accountviews
from prognosticos import views as progviews

urlpatterns = [
    path('password/', include('django.contrib.auth.urls')),

    path('app/', include('app.urls')),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    #path('rest-auth/registration/account-email-verification-sent/', accountviews.null_view, name='account_email_verification_sent'),
    #path('rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^rest-auth/registration/account-email-verification-sent/', accountviews.null_view, name='account_email_verification_sent'),
    url(r'^registration/complete/$', accountviews.complete_view, name='account_confirm_complete'),

    url(r'^salvetempo/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),


    path('admin/', admin.site.urls),

    path('sintomas/', views.SintomaList.as_view()),
    path('sintomas/<int:pk>/', views.SintomaDetail.as_view()),

    path('doencas/', views.DoencaList.as_view()),
    path('doencas/<int:pk>/', views.DoencaDetail.as_view()),

    path('paises/', views.PaisList.as_view()),
    path('paises/<int:pk>/', views.PaisDetail.as_view()),

    path('estados/', views.EstadoList.as_view()),
    path('estados/<int:pk>/', views.EstadoDetail.as_view()),

    path('cidades/', views.CidadeList.as_view()),
    path('cidades/<int:pk>/', views.CidadeDetail.as_view()),

    path('enderecos/', views.EnderecoList.as_view()),
    path('enderecos/<int:pk>/', views.EnderecoDetail.as_view()),

    path('unidades_saude/', views.UnidadeSaudeList.as_view()),
    path('unidades_saude/<int:pk>/', views.UnidadeSaudeDetail.as_view()),

    path('especializacoes/', views.EspecializacaoList.as_view()),
    path('especializacoes/<int:pk>/', views.EspecializacaoDetail.as_view()),

    path('especializacoes_doencas/', views.EspecializacaoDoencaList.as_view()),
    path('especializacoes_doencas/<int:pk>/', views.EspecializacaoDoencaDetail.as_view()),
    path('valid_especializacoes_doencas/', views.EspecializacoesDisponiveisView.as_view()),

    path('users/', accountviews.UserList.as_view()),
    path('users/<int:pk>/', accountviews.UserDetail.as_view()),

    path('pacientes/', views.PacienteList.as_view()),
    path('pacientes/<int:pk>/', views.PacienteDetail.as_view()),

    path('medicos/', views.MedicoList.as_view()),
    path('medicos/<int:pk>/', views.MedicoDetail.as_view()),

    path('medicos_unidades_saude/', views.MedicoUnidadeSaudeList.as_view()),
    path('medicos_unidades_saude_admin/', views.MedicoUnidadeSaudeAdminList.as_view()),
    path('medicos_unidades_saude/<int:pk>/', views.MedicoUnidadeSaudeDetail.as_view()),

    path('admins_unidades_saude/', views.AdminUnidadeSaudeList.as_view()),
    path('admins_unidades_saude/<int:pk>/', views.AdminUnidadeSaudeDetail.as_view()),

    path('resposta_solicitacao/', views.RespostaSolicitacaoView.as_view()),

    path('showsintoma/', progviews.ShowSintomaView.as_view()),
    path('answersintoma/', progviews.AnswerSintomaView.as_view()),
    path('startconsulta/', progviews.StartConsulta.as_view()),
    path('returnprognosticos/', progviews.ReturnPrognosticosView.as_view()),
    path('save-prognostico/', progviews.SavePrognosticoToDb.as_view()),
    path('add-sintoma/', progviews.NewSintomaFieldToDb.as_view()),

    path('anamneses/', views.AnamneseList.as_view()),

    path('consultas/', views.ConsultaList.as_view()),
    path('consultas/<int:pk>/', views.ConsultaDetail.as_view()),

    path('consultas-sintomas/', views.ConsultaSintomaList.as_view()),
    path('consultas-sintomas/<int:pk>/', views.ConsultaSintomaDetail.as_view()),

    path('consultas-prognosticos/', views.PrognosticoList.as_view()),
    path('consultas-prognosticos/<int:pk>/', views.PrognosticoDetail.as_view()),
    

    #path('salvetempo/token/', obtain_auth_token, name='obtain-token'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
