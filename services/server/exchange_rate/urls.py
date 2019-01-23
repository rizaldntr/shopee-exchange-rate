from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ExchangeRatesDetail,
    ExchangeRatesList,
    DailyExchangeRatesDetail,
    DailyExchangeRatesList
)

app_name = 'exchange-rate'

urlpatterns = [
    path('exchange-rates/',
         ExchangeRatesList.as_view(),
         name="index"),
    path('exchange-rates/<int:pk>/',
         ExchangeRatesDetail.as_view(),
         name="detail"),
    re_path('daily-exchange-rates/$',
            DailyExchangeRatesDetail.as_view(), name="daily-detail"),
    path('daily-exchange-rates/list',
         DailyExchangeRatesList.as_view(), name="daily-list")
]


urlpatterns = format_suffix_patterns(urlpatterns)
