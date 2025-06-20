import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_create_and_list_equipment(client):
    url = reverse('equipment-list')
    data = {
        'name': 'AC 01',
        'description': 'Ar condicionado da sala',
        'type': 'Split',
        'location': 'Sala 1',
        'criticality': 'Média',
        'status': 'Operacional',
    }
    response = client.post(url, data)
    assert response.status_code == 201

    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'AC 01'
