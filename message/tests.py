from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .serializer import ClientSerializer


class TestClientApi(APITestCase):
    fixtures = [
        './fixtures/client/fixture_tag.json',
        './fixtures/client/fixture_client.json',
        './fixtures/client/fixture_link_tag_and_client.json',
        './fixtures/mailing/fixture_mailing.json',
        './fixtures/message/fixture_message.json'
    ]

    def test_get(self):
        url = reverse('statistics') + '?id=1'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

