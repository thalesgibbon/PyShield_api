from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^logs/$', views.Py_LogList.as_view(), name='pylog-list'),
    path('', views.home, name='home'),
    ]
