from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ExchangeRatesDetail,
    ExchangeRatesList
)

app_name = 'exchange-rate'

urlpatterns = [
    path('exchange-rates/',
         ExchangeRatesList.as_view(),
         name="index"),
    path('exchange-rates/<int:pk>/',
         ExchangeRatesDetail.as_view(),
         name="detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
