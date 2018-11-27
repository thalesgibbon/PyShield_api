from django.shortcuts import render
from rest_framework import generics
from .models import Py_Log_mssql
from .serializers import Py_LogSerializer


class Py_LogList(generics.ListCreateAPIView):
    queryset = Py_Log_mssql.objects.all()
    serializer_class = Py_LogSerializer


def home(request):
    return render(request, 'app/home.html')
