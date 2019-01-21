from django.conf.urls import url, include
from .views import ListExchangeRatesView

app_name = 'api'

urlpatterns = [
    url(r'', ListExchangeRatesView.as_view(), name='exchange-rates-all')
]
