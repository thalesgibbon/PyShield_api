from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from __key__ import ip
import pandas as pd
import pickle

full_tel = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#telefone.pkl")
full_score_tel = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#app_score_telefone.pkl")

class simula_score_devedor(APIView):
    def get(self, request):

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


class busca_telefone(APIView):

    def get(self, request):
        cpfcnpj = int(request.GET['devedor_cpfcnpj'])

        tel = full_tel.loc[full_tel.devedor_cpfcnpj == cpfcnpj, ['telefone_numero', 'telefone_data_cadastro', 'telefone_credor_origem']]
        score_tel = full_score_tel.loc[full_score_tel.telefone_numero.isin(tel.telefone_numero), ['telefone_numero', 'score_group']]

        merge = pd.merge(tel
                         ,score_tel
                         ,on='telefone_numero'
                         ,how='left'
                        )
        merge['score_group'] = merge.score_group.fillna('N/A')
        merge = merge.sort_values(['score_group', 'telefone_data_cadastro'], ascending=[True, False])

        if len(merge) > 150:
            dicio = {0: 'mais de 150 registros'}
        else:
            dicio = merge.to_dict('index')

        return Response(data=dicio, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'app/home.html')
