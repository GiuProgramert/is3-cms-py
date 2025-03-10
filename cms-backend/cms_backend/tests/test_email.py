import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from cms_backend.views import SendEmailView

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestSendEmailView:

    @patch('cms_backend.views.SendGridAPIClient')
    @patch('cms_backend.views.Mail')
    def test_send_email_success(self, mock_mail, mock_sendgrid, api_client):
        mock_instance = mock_sendgrid.return_value
        mock_instance.send.return_value.status_code = 202
        mock_instance.send.return_value.body = b''
        mock_instance.send.return_value.headers = {'X-Message-Id': 'abcd1234'}

        data = {
            'to_email': 'usuario@ejemplo.com',
            'subject': 'Prueba de envío',
            'content': '<p>Este es un correo de prueba.</p>'
        }
        response = api_client.post(reverse('send_email'), data, format='json')

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['status_code'] == 202
        assert response_data['headers']['X-Message-Id'] == 'abcd1234'