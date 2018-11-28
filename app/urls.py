from django.conf.urls import url
from .views import Py_LogList, simula_score_devedor

urlpatterns = [
    url(r'^logs/?$', Py_LogList.as_view(), name='logs'),
    url(r'^log/(?P<pylog_id>[0-9]+)/?$', Py_LogList.as_view(), name='log'),
    #
    url(r'^credor=(?P<id_credor>[0-9]+)' +
        r'&pessoa=(?P<id_pessoa>[0-9]+)' +
        r'&garantia=(?P<id_tipo_garantia>[0-9]+)' +
        r'&cep_uf=(?P<id_cep>[0-9]+)' +
        r'&valor=(?P<valor_pmt>[0-9]+)' +
        r'/?$', simula_score_devedor.as_view(), name='simula_score_devedor'),
    ]
