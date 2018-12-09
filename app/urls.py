from django.conf.urls import url
from .views import score_rota

urlpatterns = [
    url(r'^score_rota', score_rota.as_view(), name='score_rota'),
    ]
