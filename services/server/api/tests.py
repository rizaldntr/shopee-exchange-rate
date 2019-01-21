from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer

# Create your tests here.


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_exchange_rate(from_code="", to_code=""):
        assert from_code != ""
        assert to_code != ""
        ExchangeRates.objects.create(from_code=from_code, to_code=to_code)

    def setUp(self):
        # add test data
        self.create_exchange_rate("GBP", "USD")
        self.create_exchange_rate("USD", "GBP")
        self.create_exchange_rate("USD", "IDR")
        self.create_exchange_rate("JPY", "IDR")


class GetAllExchangeRatesTest(BaseViewTest):

    def test_get_all_exchange_rates(self):
        """
        This test ensures that all exchange rates added in the setUp method
        exist when we make a GET request to the exchange_rates/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("api:exchange-rates-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = ExchangeRates.objects.all()
        serialized = ExchangeRatesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateExchangeRatesTest(BaseViewTest):

    def test_create_exchange_rate_success(self):
        """
        This test ensures that we can create new data when make
        a POST request to exchange-rates/ endpoint
        """

        # hit the API endpoint
        response = self.client.post(
            reverse("api:create-exchange-rate", kwargs={"version": "v1"}),
            data={"from_code": "IDR", "to_code": "USD"},
            format="json"
        )

        # fetch the data from db
        expected = ExchangeRates.objects.last()
        serialized = ExchangeRatesSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_exchange_rate_failed_with_duplicate_data(self):
        """
        This test ensures that we can't create new data with duplicate data
        on database when make a POST request to exchange-rates/ endpoint
        return bad request
        """

        # hit the API endpoint
        response = self.client.post(
            reverse("api:create-exchange-rate", kwargs={"version": "v1"}),
            data={"from_code": "GBP", "to_code": "USD"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
