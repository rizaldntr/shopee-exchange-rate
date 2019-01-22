from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer

# Create your views here.


class ExchangeRatesList(APIView):
    """
    List all exchange ratess, or create a new exchange rates.
    """

    def get(self, request, format=None, version="v1"):
        queryset = ExchangeRates.objects.all()
        serializer = ExchangeRatesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, version="v1"):
        serializer = ExchangeRatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ExchangeRatesDetail(APIView):
    """
    Retrieve, update or delete a exchange rate instance.
    """

    def get_object(self, pk):
        try:
            return ExchangeRates.objects.get(pk=pk)
        except ExchangeRates.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, version="v1"):
        snippet = self.get_object(pk)
        serializer = ExchangeRatesSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None, version="v1"):
        snippet = self.get_object(pk)
        serializer = ExchangeRatesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None, version="v1"):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
