from django.conf.urls import url
from .views import Py_LogList

urlpatterns = [
    url(r'^logs/?$', Py_LogList.as_view(), name='logs'),
    url(r'^log/(?P<pylog_id>[0-9]+)/?$', Py_LogList.as_view(), name='log'),
    ]
