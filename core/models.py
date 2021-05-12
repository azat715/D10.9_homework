from django.db import models
from django.db.models import Q


class CarSelectManager(models.Manager):
    def select_car(self, query_string):
        q_query = None
        options = {}
        for key in ("manufacturer", "model", "year", "transmission", "color"):
            value = query_string.get(key)
            if value:
                if "_or_" in value:
                    one, two = value.split("_or_")
                    if q_query:
                        q_query = q_query.filter(Q(**{key: one}) | Q(**{key: two}))
                    else:
                        q_query = self.filter(Q(**{key: one}) | Q(**{key: two}))
                else:
                    options[key] = value
        if q_query:
            return q_query.filter(**options)
        return self.filter(**options)


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
    objects = CarSelectManager()

    def __repr__(self):
        return "Car({self.manufacturer}, {self.model}, {self.year}, {self.transmission}, {self.color},)".format(
            self=self
        )

    def __str__(self):
        return self.__repr__()
