from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from __key__ import ip


class simula_score_devedor(APIView):
    def get(self, request):
        import pickle
        filename = r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\modelo.app_score_devedor.pkl"

        credor = int(request.GET['id_credor'])
        pessoa = int(request.GET['id_pessoa'])
        garantia = int(request.GET['id_tipo_garantia'])
        cep = int(request.GET['id_cep'])
        valor = float(request.GET['valor_pmt'])

        loaded_model = pickle.load(open(filename, 'rb'))
        retorno = loaded_model.predict([[credor, pessoa, garantia, cep, valor]])[0].astype(int)

        dicio = {}
        dicio['valor'] = retorno
        def depara(x):
            if x <= 30:
                var = '0 ~ 30 dias'
            elif x <= 180:
                var = '30 ~ 180 dias'
            else:
                var = 'maior que 180 dias'
            return var
        dicio['classificacao'] = depara(retorno)

        return Response(data=dicio, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'app/home.html')
