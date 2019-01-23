from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import ExchangeRates, DailyExchangeRates
from .serializers import ExchangeRatesSerializer, DailyExchangeRatesSerializer

# Create your tests here.


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_exchange_rate(from_code="", to_code=""):
        assert from_code != ""
        assert to_code != ""
        return ExchangeRates.objects.create(from_code=from_code, to_code=to_code)

    @staticmethod
    def create_daily_exchange_rate(exchange_rate_id, rate, date):
        assert exchange_rate_id != ""
        assert rate != ""
        assert date != ""
        DailyExchangeRates.objects.create(
            exchange_rate=exchange_rate_id, rate=rate, date=date)

    def setUp(self):
        # add test data
        exchange_rate_1 = self.create_exchange_rate("GBP", "USD")
        exchange_rate_2 = self.create_exchange_rate("USD", "GBP")
        exchange_rate_3 = self.create_exchange_rate("USD", "IDR")
        exchange_rate_4 = self.create_exchange_rate("JPY", "IDR")

        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-08")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-07")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-06")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-05")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-04")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-03")
        self.create_daily_exchange_rate(exchange_rate_1, 1, "2018-07-02")
        self.create_daily_exchange_rate(exchange_rate_2, 1, "2018-07-02")
        self.create_daily_exchange_rate(exchange_rate_3, 1, "2018-07-02")
        self.create_daily_exchange_rate(exchange_rate_4, 1, "2018-07-02")

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
        a PUT request to exchange-rates/:id/update endpoint
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
        on database when make a PUT request to exchange-rates/:id/update
        endpoint and return bad request
        """

        # hit the API endpoint
        response = self.api_call(
            pk=1, data={"from_code": "JPY", "to_code": "IDR"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_exchange_rate_failed_with_invalid_data(self):
        """
        This test ensures that we can't update data with invalid data
        when make a PUT request to exchange-rates/:id/update endpoint
        and return bad request
        """

        # hit the API endpoint
        response = self.api_call(
            pk=1, data={"from_code": "GBP", "to_code": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateDailyExchangeRate(BaseViewTest):

    def api_call(self, data={}):
        return self.client.post(
            reverse("exchange-rate:daily-detail",
                    kwargs={"version": "v1"}),
            data=data,
            format="json"
        )

    def test_create_daily_exchange_rate_success(self):
        """
        This test ensures that we can create daily exchange rate
        when make a POST request to daily-exchange-rates endpoint
        and return 201
        """

        # hit the API endpoint
        response = self.api_call(
            data={"from_code": "JPY", "to_code": "IDR", "rate": 100, "date": "2018-07-03"})

        # fetch the data from db
        expected = DailyExchangeRates.objects.last()
        serialized = DailyExchangeRatesSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_daily_exchange_rate_failed_with_duplicate_date(self):
        """
        This test ensures that we can't create daily exchange rate
        when make a POST request to daily-exchange-rates endpoint
        with duplicate date to same exchange_rate_id and return 400
        """

        # hit the API endpoint
        response = self.api_call(
            data={"from_code": "GBP", "to_code": "USD", "rate": 100, "date": "2018-07-08"})

        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_daily_exchange_rate_failed_with_exchange_rate_data_not_found(self):
        """
        This test ensures that we can't create daily exchange rate
        when make a POST request to daily-exchange-rates endpoint
        with invalid exchange_rate_id and return 404
        """

        # hit the API endpoint
        response = self.api_call(
            data={"from_code": "RZL", "to_code": "LZR", "rate": 100, "date": "2018-07-08"})

        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_daily_exchange_rate_failed_with_invalid_data(self):
        """
        This test ensures that we can't create daily exchange rate
        when make a POST request to daily-exchange-rates endpoint
        with invalid data and return 400
        """

        # hit the API endpoint
        response = self.api_call(
            data={"from_code": "RZL", "to_code": "LZR", "date": "2018-07-08"})

        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveDailyExchangeRate(BaseViewTest):
    def api_call(self, from_code, to_code):
        return self.client.get(
            reverse("exchange-rate:daily-detail",
                    kwargs={"version": "v1"}),
            data={"from_code": from_code, "to_code": to_code},
        )

    def test_retrieve_daily_exchange_rate_success(self):
        """
        This test ensures that we can retrieve data when make
        a GET request to daily-exchange-rates/ endpoint with
        query param from_code and to_code
        """

        # hit the API endpoint
        response = self.api_call(from_code="GBP", to_code="USD")
        exchange_rate = ExchangeRates.objects.get(
            from_code="GBP", to_code="USD")
        expected = DailyExchangeRates.objects.filter(
            exchange_rate=exchange_rate)
        serialized = DailyExchangeRatesSerializer(expected, many=True)
        self.assertEqual(response.data["average"], 1.0)
        self.assertEqual(response.data["variance"], 0)
        self.assertEqual(response.data["daily_exchange_rate"], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_daily_exchange_rate_failed_with_not_found_exchange_rate(self):
        """
        This test ensures that we can't retrieve data when make
        a GET request to daily-exchange-rates/ endpoint with
        invalid query param from_code and to_code
        """

        response = self.api_call(from_code="GBP", to_code="LZR")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ListDailyExchangeRates(BaseViewTest):

    def api_call(self, data):
        return self.client.get(
            reverse("exchange-rate:daily-list",
                    kwargs={"version": "v1"}),
            data=data,
        )

    def test_get_list_daily_exchange_with_date(self):
        """
        This test ensures that we can get all data when make
        a GET request to daily-exchange-rates/list endpoint with
        query param date and return exchange rate with rate and
        average from last 7 record from the date
        """

        response = self.api_call({"date": "2018-07-08"})
        self.assertEqual(response.data[0]["rate"], 1.0)
        self.assertEqual(response.data[0]["average"], 1.0)
        self.assertEqual(response.data[1]["rate"], "insufficient data")
        self.assertEqual(response.data[2]["rate"], "insufficient data")
        self.assertEqual(response.data[3]["rate"], "insufficient data")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_daily_exchange_without_date(self):
        """
        This test ensures that we can get all data when make
        a GET request to daily-exchange-rates/list endpoint with
        query param today date and return exchange rate with rate and
        average from last 7 record from the date
        """

        response = self.api_call({})
        self.assertEqual(response.data[0]["rate"], "insufficient data")
        self.assertEqual(response.data[1]["rate"], "insufficient data")
        self.assertEqual(response.data[2]["rate"], "insufficient data")
        self.assertEqual(response.data[3]["rate"], "insufficient data")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
