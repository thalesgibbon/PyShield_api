from django.shortcuts import render
from .models import Py_Log_mssql
from .serializers import Py_LogSerializer
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status


class Py_LogList(APIView):
    def get(self, request, pylog_id):
        comments = Py_Log_mssql.objects.filter(pylog_id=pylog_id).values()
        serializer = Py_LogSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'app/home.html')
