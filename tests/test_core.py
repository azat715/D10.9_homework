import pytest
from django.core.exceptions import ValidationError

from core.models import Car, TransmissionType
from .conftest import content


@pytest.mark.django_db
def test_create_car():
    car = Car.objects.create(
        manufacturer="AVTOVAZ",
        model="Granta",
        year=2021,
        transmission=TransmissionType.MANUAL,
        color="white",
    )
    assert car.manufacturer == "AVTOVAZ"
    assert car.model == "Granta"
    assert car.year == 2021
    assert car.transmission == 1
    assert car.color == "white"
    car.save()
    car.transmission = TransmissionType.AUTOMATIC
    car.save()
    assert car.transmission == 2
    car.transmission = TransmissionType.CVT
    car.save()
    assert car.transmission == 3
    car.transmission = 4
    car.save()
    with pytest.raises(ValidationError):
        car.full_clean()


@pytest.mark.django_db
def test_fixture_db(content):
    cars = Car.objects.count()
    assert cars == 6
