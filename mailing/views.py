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
        queryset_mailing_all = MailingModel.objects.all()

        queryset_messages_group = MessageModel.objects.values('mailing_id', 'status').annotate(count_id=Count('id'))

        dict_statistics = {m.id: {"mailing": m} for m in queryset_mailing_all}

        for msg in list(queryset_messages_group):
            instance_mailing = dict_statistics[msg['mailing_id']]

            instance_mailing.setdefault('messages', {})[msg['status']] = msg['count_id']

        result = list(dict_statistics.values())

        serializer = StatisticsSerializer(data=result, many=True)

        serializer.is_valid()

        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = MailingSerializer(data=request.data)

        if serializer.is_valid():
            launch_time = serializer.data["launch_time"]
            finish_time = serializer.data["finish_time"]
            message_text = serializer.data["message_text"]
            filter_tags = serializer.data["filter_tags"]
            filter_operator = serializer.data["filter_operator"]

            mailing_instance = MailingModel.objects.create(
                launch_time=launch_time,
                finish_time=finish_time,
                message_text=message_text,
                filter_tags=filter_tags,
                filter_operator=filter_operator
            )


            scheduled_time = launch_time.replace('Z', '').split("T")
            
            date = list(map(int, scheduled_time[0].split('-')))

            time_format = scheduled_time[1].split('-')
   
            time_zone = time_format[1].split(':')

            time = list(map(int, time_format[0].split(':')))

            arr_date_time = date + time

            time_diff = datetime(*arr_date_time) - datetime.now()

            current_app.send_task('mailing.tasks.mailing_task', args=[mailing_instance.id], eta=datetime.now() + time_diff - timedelta(hours=int(time_zone[0]), minutes=int(time_zone[1])))

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        mailing_id = request.GET.get("id")

        instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        serializer = MailingSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        mailing_id = request.GET.get("id")

        instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
