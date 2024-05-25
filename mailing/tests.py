from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .utils.format_date import string_to_arrays_int
from .utils.task import create_task
from .models import MailingModel, CeleryTaskModel
from .serializer import MailingSerializer, StatisticsSerializer

from datetime import datetime


class TestClientApi(APITestCase):
    fixtures = [
        './fixtures/client/fixture_tag.json',
        './fixtures/client/fixture_client.json',
        './fixtures/client/fixture_link_tag_and_client.json',
        './fixtures/mailing/fixture_mailing.json',
        './fixtures/mailing/fixture_task.json',
        './fixtures/message/fixture_message.json',
    ]
    
    def test_get(self):
        url = reverse('mailing')

        response = self.client.get(url)   

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_utils_format_date(self):
        date_time = '2023-12-09T17:25:00-06:00'

        arr_date_time = string_to_arrays_int(date_time)

        self.assertEqual(arr_date_time, ([2023, 12, 9, 17, 25, 0], [6, 0]))

    def test_utils_task(self):
        mailing = MailingModel.objects.get(id=1)

        arr_date_time, time_zone = string_to_arrays_int(str(mailing.launch_time))

        time_diff = datetime(*arr_date_time) - datetime.now()

        task = create_task(mailing, time_diff, time_zone)

        self.assertIsInstance(task, CeleryTaskModel)