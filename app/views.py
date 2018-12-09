from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from __config__ import change_in_latitude, m_to_miles


bo = pd.read_pickle("C:\PyShield\data\#TransformBO.pkl")
gmaps = pd.read_pickle("C:\PyShield\data\#request_gmaps.pkl")


class score_rota(APIView):
    def get(self, request):
        rotas = str(request.GET['rotas'])
        print(rotas)

        desvio_padrao = change_in_latitude(m_to_miles(20))

        tot = pd.DataFrame()
        for registro in range(len(gmaps)):

            calc = bo[(bo.LATITUDE.between(gmaps.loc[registro, 'start_loc_lat'] - desvio_padrao,
                                           gmaps.loc[registro, 'end_loc_lat'] + desvio_padrao)) & (
                          bo.LONGITUDE.between(gmaps.loc[registro, 'start_loc_lng'] - desvio_padrao,
                                               gmaps.loc[registro, 'end_loc_lng'] + desvio_padrao))]
            calc['ind'] = registro

            tot = pd.concat([calc, tot])

        valor_relativo = 6
        numero_estrelas_score = 5

        dicio = {'score': (numero_estrelas_score - min(len(tot) / valor_relativo, numero_estrelas_score))}

        return Response(data=dicio, status=status.HTTP_200_OK)
