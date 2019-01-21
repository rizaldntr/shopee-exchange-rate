from rest_framework import generics
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer

# Create your views here.


class ListExchangeRatesView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = ExchangeRates.objects.all()
    serializer_class = ExchangeRatesSerializer
