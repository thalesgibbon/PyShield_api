from django.shortcuts import render
from .models import Py_Log_mssql
from .serializers import Py_LogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from __key__ import ip


class Py_LogList(APIView):
    def get(self, request, pylog_id):
        comments = Py_Log_mssql.objects.filter(pylog_id=pylog_id).values()
        serializer = Py_LogSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class simula_score_devedor(APIView):
    def get(self, request, id_credor, id_pessoa, id_tipo_garantia, id_cep, valor_pmt):
        import pickle
        filename = r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\modelo.app_score_devedor.pkl"

        credor = int(id_credor)
        pessoa = int(id_pessoa)
        garantia = int(id_tipo_garantia)
        cep = int(id_cep)
        valor = float(valor_pmt)

        loaded_model = pickle.load(open(filename, 'rb'))
        retorno = loaded_model.predict([[credor, pessoa, garantia, cep, valor]])[0].astype(int)

        return Response(data=retorno, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'app/home.html')
