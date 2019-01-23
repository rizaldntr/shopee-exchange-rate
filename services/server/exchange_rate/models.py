from django.db import models

# Create your models here.


class ExchangeRates(models.Model):
    class Meta:
        unique_together = ("from_code", "to_code")

    # from code exchange rate
    from_code = models.CharField(max_length=255, null=False)
    # to code exchange rate
    to_code = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.from_code, self.to_code)


class DailyExchangeRates(models.Model):
    class Meta:
        unique_together = ("date", "exchange_rate")

    # rate
    rate = models.FloatField()
    # date the daily exchange rate
    date = models.DateField()
    # foreign key to model ExchangeRates
    exchange_rate = models.ForeignKey(ExchangeRates, on_delete=models.CASCADE)
