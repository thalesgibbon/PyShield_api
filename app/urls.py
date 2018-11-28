from django.conf.urls import url
from .views import simula_score_devedor

urlpatterns = [
    url(r'^simulacao', simula_score_devedor.as_view(), name='simulacao'),
    ]
