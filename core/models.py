from django.db import models


class TransmissionType(models.IntegerChoices):
    MANUAL = 1, "Manual"
    AUTOMATIC = 2, "Automatic"
    CVT = 3, "CVT"


class Car(models.Model):
    manufacturer = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    transmission = models.SmallIntegerField(choices=TransmissionType.choices)
    color = models.CharField(max_length=30)
