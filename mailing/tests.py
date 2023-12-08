from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .serializer import MailingSerializer, StatisticsSerializer


class TestClientApi(APITestCase):
    fixtures = [
        './fixtures/client/fixture_tag.json',
        './fixtures/client/fixture_client.json',
        './fixtures/client/fixture_link_tag_and_client.json',
        './fixtures/mailing/fixture_mailing.json',
        './fixtures/message/fixture_message.json'
    ]
    
    def test_get(self):
        url = reverse('mailing')

        response = self.client.get(url)   

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('mailing')

        data = {
            "launch_time": "2023-12-01T12:00:00Z",
            "finish_time": "2023-12-10T18:00:00Z",
            "message_text": "Привет, мир!",
            "filter_tags": [1, 2],
            "filter_operator": "777"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        url = reverse('mailing') + '?id=1'

        data = {
            "launch_time": "2023-12-01T12:00:00Z",
            "finish_time": "2023-12-10T18:00:00Z",
            "message_text": "Привет, мир!",
            "filter_tags": [1, 2],
            "filter_operator": "777"
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('mailing') + '?id=1'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_mailing_serializer(self):
        data = {
            "launch_time": "2023-12-01T12:00:00Z",
            "finish_time": "2023-12-10T18:00:00Z",
            "message_text": "Привет, мир!",
            "filter_tags": [1, 2],
            "filter_operator": "777"
        }
        
        result = MailingSerializer(data=data)

        self.assertEqual(result.is_valid(), True)

    def test_statistics_serializer(self):
        data = {
            "mailing": {
                "launch_time": "2023-12-01T06:00:00-06:00",
                "finish_time": "2023-12-10T12:00:00-06:00",
                "message_text": "Привет, мир!",
                "filter_tags": [
                    1,
                    2
                ],
                "filter_operator": "771"
            },
            "messages": {
                "Delivered": 2
            }
        }

        result = StatisticsSerializer(data=data)

        self.assertEqual(result.is_valid(), True)    
