from django.shortcuts import get_object_or_404

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

    def create(self, request, version="v1"):
        serializer = ExchangeRatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Data is invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, version="v1", pk=None):
        exchange_rate = get_object_or_404(ExchangeRates, id=pk)
        exchange_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
