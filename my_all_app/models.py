from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Indicator(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    user = models.IntegerField(unique=False, null=True)

    def __str__(self, **kwargs):
        return self.name

    def retrurnName(self):
        return self.name

    def retrurnDescription(self):
        return self.description


class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.IntegerField(unique=False, null=True)

    def __str__(self):
        return self.name

    def retrurnName(self):
        return self.name


class Position(models.Model):
    #position_index = models.ForeignKey(Index, on_delete=models.CASCADE, null=True)
    volume = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(10)],)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    sl = models.FloatField(null=True)
    be = models.FloatField(null=True)
    tp1 = models.FloatField(null=True)
    tp2 = models.FloatField(null=True)
    tp3 = models.FloatField(null=True)
    position_indicator = models.ManyToManyField(Indicator)
    comment = models.TextField(null=True)
    status = models.CharField(max_length=20, null=True)
    user = models.IntegerField(unique=False, null=True)

    def returnIndicator(self):
        return self.position_indicator.name

