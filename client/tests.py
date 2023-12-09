from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .serializer import ClientSerializer
from .models import ClientModel
from .utils.link_tags import create_link_tags


class TestClientApi(APITestCase):
    fixtures = [
        './fixtures/client/fixture_tag.json',
        './fixtures/client/fixture_client.json',
        './fixtures/client/fixture_link_tag_and_client.json'
    ]

    def test_post(self):
        url = reverse('client')

        data = {
            "phone_number": "+77519009887",
            "timezone": 'UTC',
            "tags": [1]
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        url = reverse('client') + '?id=1'

        data = {
            "phone_number": "+77519009887",
            "timezone": 'UTC',
            "tags": [1]
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('client') + '?id=1'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_serializer(self):
        data = {
            "phone_number": "+77519009887",
            "timezone": 'UTC',
            "tags": [1]
        }
        
        result = ClientSerializer(data=data)

        self.assertEqual(result.is_valid(), True)

    def test_utils_link_tags(self):
        client = ClientModel.objects.get(id=1)

        links = create_link_tags(client, [1, 2])

        tags = ['customer', 'partner']

        for link, tag in zip(links, tags):
            self.assertEqual(link.tag.mark, tag)
