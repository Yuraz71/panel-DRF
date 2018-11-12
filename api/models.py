from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Panel(models.Model):
    # Brand is not required by Project Tasks
    brand = models.CharField(max_length=200, blank=True)
    serial = models.CharField(max_length=16)
    latitude = models.DecimalField(decimal_places=6,max_digits=8)
    longitude = models.DecimalField(decimal_places=6,max_digits=9)
    def __str__(self):
        return "Brand: {0}, Serial: {1} ".format(self.brand, self.serial)

class OneHourElectricity(models.Model):
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    kilo_watt = models.BigIntegerField()
    date_time_db = models.DateTimeField()
    def __str__(self):
        return "Hour: {0} - {1} KiloWatt".format(self.date_time_db, self.kilo_watt)
