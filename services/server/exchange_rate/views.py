import math
import datetime

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from .models import ExchangeRates, DailyExchangeRates
from .serializers import ExchangeRatesSerializer, DailyExchangeRatesSerializer

# Create your views here.


class ExchangeRatesList(APIView):
    """
    List all exchange ratess, or create a new exchange rates.
    """

    def get(self, request, format=None, version="v1"):
        queryset = ExchangeRates.objects.all()
        serializer = ExchangeRatesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, version="v1"):
        serializer = ExchangeRatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ExchangeRatesDetail(APIView):
    """
    Retrieve, update or delete a exchange rate instance.
    """

    def get_object(self, pk):
        try:
            return ExchangeRates.objects.get(pk=pk)
        except ExchangeRates.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, version="v1"):
        exchange_rate = self.get_object(pk)
        serializer = ExchangeRatesSerializer(exchange_rate)
        return Response(serializer.data)

    def put(self, request, pk, format=None, version="v1"):
        exchange_rate = self.get_object(pk)
        serializer = ExchangeRatesSerializer(exchange_rate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None, version="v1"):
        exchange_rate = self.get_object(pk)
        exchange_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DailyExchangeRatesDetail(APIView):
    """
    Detail daily exchange rates, or create a new daily exchange rates.
    """

    def get_object(self, from_code, to_code):
        try:
            return ExchangeRates.objects.get(
                from_code=from_code, to_code=to_code)
        except ExchangeRates.DoesNotExist:
            raise Http404

    def get_variance_and_average(self, daily_exchange_rate):
        sum_rate = 0
        min_rate = math.inf
        max_rate = -math.inf
        for data in daily_exchange_rate:
            sum_rate = sum_rate + data.rate
            if data.rate < min_rate:
                min_rate = data.rate
            if data.rate > max_rate:
                max_rate = data.rate
        average = sum_rate/len(daily_exchange_rate)
        variance = max_rate - min_rate
        return (variance, average)

    def get(self, request, format=None, version="v1"):
        from_code = request.query_params.get('from_code', '')
        to_code = request.query_params.get('to_code', '')
        exchange_rate = self.get_object(from_code, to_code)

        daily_exchange_rate = DailyExchangeRates.objects.filter(
            exchange_rate=exchange_rate).order_by('-date')[:7]
        daily_exchange_rate_serializer = DailyExchangeRatesSerializer(
            daily_exchange_rate, many=True)
        exchange_rate_serializer = ExchangeRatesSerializer(exchange_rate)
        variance, average = self.get_variance_and_average(daily_exchange_rate)
        data = {'exchange_rate': exchange_rate_serializer.data,
                'daily_exchange_rate': daily_exchange_rate_serializer.data,
                'variance': variance,
                'average': average
                }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None, version="v1"):
        try:
            from_code = request.data['from_code']
            to_code = request.data['to_code']
            rate = request.data['rate']
            date = request.data['date']
        except Exception:
            return Response({'errors': 'Your request is invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        exchange_rate = self.get_object(from_code, to_code)
        data = {'exchange_rate': exchange_rate.id, 'rate': rate, 'date': date}

        serializer = DailyExchangeRatesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class DailyExchangeRatesList(APIView):
    """
    List daily exchange rates
    """

    def get_average_rate(self, daily_exhange_rate):
        sum_rate = 0
        for data in daily_exhange_rate:
            sum_rate = sum_rate + data.rate

        return sum_rate/len(daily_exhange_rate)

    def get_daily_exchange_rate(self, exchange_rate, date, last_week_date):
        return DailyExchangeRates.objects.filter(
            exchange_rate=exchange_rate.id,
            date__range=[last_week_date, date]).order_by("-date")

    def get(self, request, format=None, version="v1"):
        date = request.query_params.get('date', None)
        if date is None:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

        last_week_date = date - datetime.timedelta(days=7)

        exchange_rate = ExchangeRates.objects.all()
        datas = []
        for data in exchange_rate:
            daily_exchange_rate = self.get_daily_exchange_rate(
                data, date, last_week_date)
            if len(daily_exchange_rate) < 7:
                average = ""
                rate = "insufficient data"
            else:
                average = self.get_average_rate(daily_exchange_rate)
                rate = daily_exchange_rate[0].rate
            tmp_data = {'average': average, 'rate': rate}
            exchange_rate_serializer = ExchangeRatesSerializer(data)
            tmp_data.update(exchange_rate_serializer.data)
            datas.append(tmp_data)

        return Response(data=datas, status=status.HTTP_200_OK)
