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
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    path('app/', include('app.urls')),
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
]

urlpatterns = format_suffix_patterns(urlpatterns)
