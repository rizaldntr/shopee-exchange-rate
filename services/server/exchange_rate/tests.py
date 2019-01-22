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

    def get_list_or_detail_serialized_data_from_db(self, pk=None):
        if pk is None:
            data = ExchangeRates.objects.all()
            return ExchangeRatesSerializer(data, many=True)

        data = ExchangeRates.objects.get(id=pk)
        return ExchangeRatesSerializer(data)

    def get_data_size(self):
        data = ExchangeRates.objects.all()
        return len(data)


class GetAllExchangeRatesTest(BaseViewTest):

    def test_get_all_exchange_rates(self):
        """
        This test ensures that all exchange rates added in the setUp method
        exist when we make a GET request to the exchange_rates/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("exchange-rate:index", kwargs={"version": "v1"})
        )
        # fetch the data from db
        serialized = self.get_list_or_detail_serialized_data_from_db()
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateExchangeRatesTest(BaseViewTest):

    def api_call(self, data={}):
        return self.client.post(
            reverse("exchange-rate:index", kwargs={"version": "v1"}),
            data=data,
            format="json"
        )

    def test_create_exchange_rate_success(self):
        """
        This test ensures that we can create new data when make
        a POST request to exchange-rates/ endpoint
        """

        # hit the API endpoint
        response = self.api_call(data={"from_code": "IDR", "to_code": "USD"})

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
        response = self.api_call(data={"from_code": "GBP", "to_code": "USD"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_exchange_rate_failed_with_invalid_data(self):
        """
        This test ensures that we can't create new data with invalid data
        when make a POST request to exchange-rates/ endpoint return bad
        request
        """

        # hit the API endpoint
        response = self.api_call(data={"from_code": "GBP", "to_code": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteExchangeRatesTest(BaseViewTest):

    def api_call(self, pk=None):
        return self.client.delete(
            reverse("exchange-rate:detail",
                    kwargs={"version": "v1", "pk": pk})
        )

    def test_delete_exchange_rate_success(self):
        """
        This test ensures that we can delete data when make
        a DELETE request to exchange-rates/:id endpoint with
        valid id
        """

        # fetch old data before API call
        old_data_size = self.get_data_size()

        # hit the API endpoint
        response = self.api_call(pk=1)

        # fetch new data after API call
        new_data_size = self.get_data_size()
        self.assertEqual(old_data_size - 1, new_data_size)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_exchange_rate_failed_wtih_invalid_id(self):
        """
        This test ensures that we can delete data when make
        a DELETE request to exchange-rates/:id endpoint with
        invalid id
        """

        # fetch old data before API call
        old_data_size = self.get_data_size()

        # hit the API endpoint
        response = self.api_call(pk=9999)

        # fetch new data before API call
        new_data_size = self.get_data_size()
        self.assertEqual(old_data_size, new_data_size)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RetrieveExchangeRatesTest(BaseViewTest):

    def api_call(self, pk=None):
        return self.client.get(
            reverse("exchange-rate:detail",
                    kwargs={"version": "v1", "pk": pk})
        )

    def test_retrieve_exchange_rate_success_wtih_valid_id(self):
        """
        This test ensures that we can't retrieve data when make
        a GET request to exchange-rates/:id endpoint with
        valid id
        """

        # hit the API endpoint
        response = self.api_call(pk=1)

        # fetch db
        serialized = self.get_list_or_detail_serialized_data_from_db(pk=1)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_exchange_rate_failed_wtih_invalid_id(self):
        """
        This test ensures that we can't retrieve data when make
        a GET request to exchange-rates/:id endpoint with
        invalid id
        """

        # hit the API endpoint
        response = self.api_call(pk=1000)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateExchangeRatesTest(BaseViewTest):

    def api_call(self, pk=None, data={}):
        return self.client.put(
            reverse("exchange-rate:detail",
                    kwargs={"version": "v1", "pk": pk}),
            data=data,
            format="json"
        )

    def test_update_exchange_rate_success(self):
        """
        This test ensures that we can update data when make
        a POST request to exchange-rates/:id/update endpoint
        """

        # hit the API endpoint
        response = self.api_call(
            pk=1, data={"from_code": "DZD", "to_code": "EUR"})

        # fetch the data from db
        serialized = self.get_list_or_detail_serialized_data_from_db(pk=1)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_exchange_rate_failed_with_duplicate_data(self):
        """
        This test ensures that we can't update data with duplicate data
        on database when make a POST request to exchange-rates/:id/update
        endpoint and return bad request
        """

        # hit the API endpoint
        response = self.api_call(
            pk=1, data={"from_code": "JPY", "to_code": "IDR"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_exchange_rate_failed_with_invalid_data(self):
        """
        This test ensures that we can't update data with invalid data
        when make a POST request to exchange-rates/:id/update endpoint
        and return bad request
        """

        # hit the API endpoint
        response = self.api_call(
            pk=1, data={"from_code": "GBP", "to_code": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
