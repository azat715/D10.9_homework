import pytest

from core.models import Car, TransmissionType


@pytest.fixture(scope="session")
def content(django_db_setup, django_db_blocker):
    """
    заполение базы данных
    """
    with django_db_blocker.unblock():
        Car.objects.bulk_create(
            [
                Car(
                    manufacturer="AVTOVAZ",
                    model="Granta",
                    year=2020,
                    transmission=TransmissionType.AUTOMATIC,
                    color="red",
                ),
                Car(
                    manufacturer="AVTOVAZ",
                    model="Vesta",
                    year=2019,
                    transmission=TransmissionType.CVT,
                    color="orange",
                ),
                Car(
                    manufacturer="AVTOVAZ",
                    model="X Ray",
                    year=2021,
                    transmission=TransmissionType.AUTOMATIC,
                    color="yellow",
                ),
                Car(
                    manufacturer="Kia",
                    model="Rio",
                    year=2019,
                    transmission=TransmissionType.MANUAL,
                    color="green",
                ),
                Car(
                    manufacturer="Kia",
                    model="Ceed",
                    year=2021,
                    transmission=TransmissionType.AUTOMATIC,
                    color="blue",
                ),
                Car(
                    manufacturer="Kia",
                    model="Ceed",
                    year=2020,
                    transmission=TransmissionType.CVT,
                    color="cyan",
                ),
            ]
        )
