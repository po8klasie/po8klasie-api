import pytest

from search.load_data import insert_publiczne_oddzialy_2020
from search.models import School


@pytest.mark.django_db
def test_insert_publiczne_oddzialy_2020():
    insert_publiczne_oddzialy_2020()
    assert School.objects.all().count() == 1044
