from django.conf.urls import url, include
from .views import ExchangeRatesViewSet

app_name = 'api'

urlpatterns = [
    url(r'^$', ExchangeRatesViewSet.as_view(
        {'get': 'list'}), name='exchange-rates-all'),
    url(r'^create$', ExchangeRatesViewSet.as_view(
        {'post': 'create'}), name='create-exchange-rate'),
    url(r'^(?P<pk>\d+)/delete$', ExchangeRatesViewSet.as_view(
        {'delete': 'destroy'}), name='delete-exchange-rate'),
]
