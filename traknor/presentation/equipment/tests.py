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


def _upload_csv(client, content: str):
    from django.core.files.uploadedfile import SimpleUploadedFile

    file = SimpleUploadedFile(
        "eq.csv",
        content.encode("utf-8"),
        content_type="text/csv",
    )
    url = reverse("equipment-import")
    return client.post(url, {"file": file})


def test_import_valid_csv(client):
    csv_data = (
        "name,description,type,location,criticality,status\n"
        "AC1,Desc,Split,Room,Alta,Operacional\n"
        "AC2,Desc,Fancoil,Room,Média,Operacional\n"
    )
    response = _upload_csv(client, csv_data)
    assert response.status_code == 200
    assert response.json()["created"] == 2
    assert response.json()["errors"] == []


def test_import_csv_with_errors(client):
    csv_data = (
        "name,description,type,location,criticality,status\n"
        "AC1,Desc,Invalid,Room,Alta,Operacional\n"
    )
    response = _upload_csv(client, csv_data)
    assert response.status_code == 400
    assert response.json()["created"] == 0
    assert len(response.json()["errors"]) == 1
