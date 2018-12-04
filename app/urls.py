from django.conf.urls import url
from .views import simula_score_devedor, busca_telefone

urlpatterns = [
    url(r'^simulacao', simula_score_devedor.as_view(), name='simulacao'),
    url(r'^busca_telefone', busca_telefone.as_view(), name='busca_telefone'),
    ]
