from rest_framework import serializers
from .models import Py_Log_mssql


class Py_LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Py_Log_mssql
        fields = '__all__'
