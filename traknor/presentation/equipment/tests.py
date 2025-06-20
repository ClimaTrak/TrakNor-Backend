import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_index(client):
    url = reverse('equipment:index')
    response = client.get(url)
    assert response.status_code == 200


