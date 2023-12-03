from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import views, permissions, status
from rest_framework.response import Response

from message.models import MessageModel

from .models import MailingModel
from .serializer import MailingSerializer, StatisticsSerializer

from datetime import datetime, timedelta
from celery import current_app


class MailingApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        mailing_all = MailingModel.objects.all()

        queryset = MessageModel.objects.values('mailing_id', 'status').annotate(count_id=Count('id'))

        dict_statistics = {m.id: {"mailing": m} for m in mailing_all}

        for msg in list(queryset):
            instance_messages = dict_statistics[msg["mailing_id"]].get('messages', '')

            if instance_messages:
                instance_messages[msg["status"]] = msg["count_id"]
            else:
                dict_statistics[msg["mailing_id"]]['messages'] = {msg["status"]: msg["count_id"]}

        dict_statistics = [v for k, v in dict_statistics.items()]

        ser = StatisticsSerializer(data=dict_statistics, many=True)

        ser.is_valid()

        return Response(ser.data)


    def post(self, request, *args, **kwargs):
        serializer = MailingSerializer(data=request.data)

        if serializer.is_valid():
            launch_time = serializer.data["launch_time"]
            finish_time = serializer.data["finish_time"]
            message_text = serializer.data["message_text"]
            filter_tags = serializer.data["filter_tags"]
            filter_operator = serializer.data["filter_operator"]

            MailingModel.objects.create(
                launch_time=launch_time,
                finish_time=finish_time,
                message_text=message_text,
                filter_tags=filter_tags,
                filter_operator=filter_operator
            )

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ClientModel, pk)

        serializer = MailingSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        id = request.GET.get("id")

        print(id)

        instance = get_object_or_404(klass=MailingModel, pk=id)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TestCeleryView(views.APIView):
    def post(self, request, *args, **kwargs):
        # Получите время из запроса, например:
        scheduled_time = request.data.get('scheduled_time').split()

        print(1)

        date = list(map(int, scheduled_time[0].split('.')))
        time = list(map(int, scheduled_time[1].split(':')))

        arr_date_time = date + time

        # Рассчитайте разницу между текущим временем и временем выполнения
        time_diff = datetime(*arr_date_time) - datetime.now()

        print(datetime.now() + time_diff - timedelta(hours=6))

        # Запланируйте выполнение задачи с использованием Celery
        current_app.send_task('mailing.tasks.your_task', eta=datetime.now() + time_diff)

        return Response({'message': 'Задача запланирована успешно'})
