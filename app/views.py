from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from __key__ import ip
import pandas as pd
import pickle


full_devedor = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#devedor.pkl")
full_titulo = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#titulo.pkl")
full_pmt = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#movimento_parcela.pkl")
full_credor = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#credor.pkl")
full_tel = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#telefone.pkl")
full_score_tel = pd.read_pickle(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\#app_score_telefone.pkl")
loaded_model = pickle.load(open(r'\\' + ip['ip_thanus_fonte'] + r"\ProjetosDW\data\load\modelo.app_score_devedor.pkl", 'rb'))


def df_dict_depara(df, asc=True):
    if asc:
        df = df[[df.columns[0], df.columns[1]]]
    else:
        df = df[[df.columns[1], df.columns[0]]]
    depara = df.set_index(df.columns[0])
    depara = depara[depara.columns[0]].to_dict()
    return depara


class simula_score_devedor(APIView):
    def get(self, request):
        credor = int(request.GET['id_credor'])
        pessoa = int(request.GET['id_pessoa'])
        garantia = int(request.GET['id_tipo_garantia'])
        cep = int(request.GET['id_cep'])
        valor = float(request.GET['valor_pmt'])

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


class busca_contrato(APIView):
    def get(self, request):
        from numpy import where
        cpfcnpj = int(request.GET['devedor_cpfcnpj'])

        dev = full_devedor.loc[full_devedor.devedor_cpfcnpj == cpfcnpj, ['devedor_full', 'chave_devedor', 'devedor_cpfcnpj']]
        tit = full_titulo.loc[full_titulo.chave_devedor.isin(dev.chave_devedor), ['chave_titulo', 'chave_credor', 'chave_devedor', 'titulo_contrato', 'titulo_qtde']]
        pmt = full_pmt.loc[full_pmt.chave_titulo.isin(tit.chave_titulo), ['chave_movimento', 'chave_titulo', 'movimento_baixa_id', 'movimento_pmt_valor']]

        merge = pd.merge(pmt
                         ,tit
                         ,on='chave_titulo'
                         ,how='left'
                        )
        merge = pd.merge(merge
                         ,dev
                         ,on='chave_devedor'
                         ,how='left'
                        )
        depara = df_dict_depara(full_credor[['chave_credor', 'credor_full']])

        merge['movimento_baixa'] = where(merge.movimento_baixa_id == 0, 'ABERTO', 'BAIXADO')
        del merge['movimento_baixa_id']

        merge['credor'] = merge.chave_credor.map(depara).fillna('N/A')
        del merge['chave_credor']

        merge_agg = merge.groupby(['movimento_baixa', 'credor', 'chave_titulo'], as_index=False)['movimento_pmt_valor', 'titulo_qtde'].sum()
        del merge

        merge_agg['movimento_pmt_valor'] = merge_agg.movimento_pmt_valor.apply(lambda x: float(format(x, '.2f')))

        if len(merge_agg) > 150:
            dicio = {0: 'mais de 150 registros'}
        else:
            dicio = merge_agg.to_dict('index')

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
        depara = df_dict_depara(full_credor[['chave_credor', 'credor_full']])
        merge['telefone_credor_origem'] = merge.telefone_credor_origem.map(depara).fillna('N/A')
        merge['score_group'] = merge.score_group.fillna('N/A')
        merge['telefone_data_cadastro'] = merge.telefone_data_cadastro.dt.strftime('%Y-%m-%d')
        merge = merge.sort_values(['score_group', 'telefone_data_cadastro'], ascending=[True, False])

        if len(merge) > 150:
            dicio = {0: 'mais de 150 registros'}
        else:
            dicio = merge.to_dict('index')

        return Response(data=dicio, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'app/home.html')
