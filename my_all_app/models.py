from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Indicator(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    user = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name


class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.IntegerField(unique=True, null=True)



class Position(models.Model):
    position_index = models.OneToOneField(Index, on_delete=models.CASCADE, null=True)
    volume = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(10)],)
    price = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    be = models.FloatField()
    tp1 = models.FloatField()
    tp2 = models.FloatField()
    tp3 = models.FloatField()
    position_indicator = models.ManyToManyField(Indicator)
    comment = models.TextField(null=True)
    user = models.IntegerField(unique=True, null=True)



