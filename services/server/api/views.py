from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer

# Create your views here.


class ExchangeRatesViewSet(viewsets.ViewSet):
    """
    ViewSet exchange-rates api
    """

    def list(self, request, version="v1"):
        queryset = ExchangeRates.objects.all()
        serializer = ExchangeRatesSerializer(queryset, many=True)
        return Response(serializer.data)
