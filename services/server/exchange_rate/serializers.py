from rest_framework import serializers
from .models import ExchangeRates, DailyExchangeRates


class ExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = ("id", "from_code", "to_code")


class DailyExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyExchangeRates
        fields = ("id", "exchange_rate", "rate", "date")
