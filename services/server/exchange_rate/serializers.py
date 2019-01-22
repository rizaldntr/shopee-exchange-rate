from rest_framework import serializers
from .models import ExchangeRates


class ExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = ("id", "from_code", "to_code")
