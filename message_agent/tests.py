from django.urls import reverse
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
def test_api_create_message():
    client = APIClient()
    url = reverse('message_agent:api_create_message')
    data = {
        "content": "-----BEGIN PGP MESSAGE-----\n...\n-----END PGP MESSAGE-----",
        "note": "test note",
        "password": "testpass"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201  # 或 200，视你的实现
    assert "short_id" in response.data