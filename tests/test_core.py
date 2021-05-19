import pytest
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.db.models import Q
from django.core.serializers import serialize

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


@pytest.mark.django_db
def test_car_fields_value(content):
    cars = Car.objects.fields_value()
    assert cars == {
        "manufacturer": ["AVTOVAZ", "Kia"],
        "model": ["Granta", "Vesta", "X Ray", "Rio", "Ceed"],
        "year": [2020, 2019, 2021],
        "color": ["red", "orange", "yellow", "green", "blue", "cyan"],
    }


# @pytest.fixture()
# def query_simple():
#     return QueryDict(
#         "manufacturer=AVTOVAZ&model=Vesta&year=2019&transmission=3&color=orange"
#     )


# @pytest.fixture()
# def query_or():
#     return QueryDict("model=Vesta_OR_Granta")


# # @pytest.fixture()
# # def query_fixture():
# #     return QueryDict("model=Vesta&year=2019")


# @pytest.mark.django_db
# def test_select_car(content, query_simple):
#     select = Car.objects.select_car(query_simple)
#     select_check = Car.objects.filter(
#         manufacturer="AVTOVAZ", model="Vesta", year=2019, transmission=3, color="orange"
#     )
#     assert select.__repr__() == select_check.__repr__()


# @pytest.mark.django_db
# def test_select_car_q(content, query_or):
#     select = Car.objects.select_car(query_or)
#     select_check = Car.objects.filter((Q(model="Vesta") | Q(model="Granta")))
#     print(select)
#     assert False
#     # assert select.__repr__() == select_check.__repr__()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query_or,select_check",
    [
        (
            QueryDict(
                "manufacturer=AVTOVAZ&model=Vesta&year=2019&transmission=3&color=orange"
            ),
            Car.objects.filter(
                manufacturer="AVTOVAZ",
                model="Vesta",
                year=2019,
                transmission=3,
                color="orange",
            ),
        ),
        (
            QueryDict("model=Vesta_OR_Granta"),
            Car.objects.filter((Q(model="Vesta") | Q(model="Granta"))),
        ),
        (
            QueryDict("manufacturer=AVTOVAZ&transmission=2_OR_3"),
            Car.objects.filter(
                (Q(transmission=2) | Q(transmission=3)), manufacturer="AVTOVAZ"
            ),
        ),
        (
            QueryDict("manufacturer=AVTOVAZ_OR_Kia&transmission=2"),
            Car.objects.filter(
                (Q(manufacturer="AVTOVAZ") | Q(manufacturer="Kia")), transmission=2
            ),
        ),
        (
            QueryDict("manufacturer=AVTOVAZ_OR_Kia&year=2020_OR_2021"),
            Car.objects.filter(
                Q(manufacturer="AVTOVAZ") | Q(manufacturer="Kia"),
                Q(year=2020) | Q(year=2021),
            ),
        ),
    ],
)
def test_select_car(content, query_or, select_check):
    select = Car.objects.select_car(query_or)
    assert select.__repr__() == select_check.__repr__()


@pytest.mark.django_db
@pytest.mark.skipif(False, reason="экспорт базы в fixture.json")
def test_fixture_to_json(content, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with open("fixture.json", "w") as f:
            f.write(serialize("json", list(Car.objects.all())))
