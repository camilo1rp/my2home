from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    iso2 = models.CharField(max_length=10)
    iso3 = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    code = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    code = models.IntegerField()

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


