from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import views, status, serializers
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, OpenApiParameter

from message.models import MessageModel

from .models import MailingModel, CeleryTaskModel
from .serializer import MailingSerializer, StatisticsSerializer
from .utils.format_date import string_to_arrays_int
from .utils.task import create_task

from datetime import datetime
from celery import current_app


class MailingApiView(views.APIView):
    @extend_schema(
        request=StatisticsSerializer,
        responses={
            200: OpenApiResponse(
                response=StatisticsSerializer(many=True),
                examples=[
                    OpenApiExample(
                        name="Example",
                        value={
                            "mailing": {
                                "launch_time": "2023-12-09T17:04:04.121Z",
                                "finish_time": "2023-12-09T17:04:04.121Z",
                                "message_text": "string",
                                "filter_tags": [1, 2],
                                "filter_operator": 777
                                },
                            "messages": {
                                "Delivered": 3,
                                "Failed": 1
                            }
                        },
                    )
                ]
            )
        }
    )
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

    @extend_schema(
        request=MailingSerializer,
        responses={
            201: OpenApiResponse(),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="Error input data",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
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

            arr_date_time, time_zone = string_to_arrays_int(launch_time)

            time_diff = datetime(*arr_date_time) - datetime.now()

            create_task(mailing_instance, time_diff, time_zone)

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=MailingSerializer,
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='Description of the query parameter',
                required=True,
            ),
        ],
        responses={
            201: MailingSerializer(),
            404: OpenApiResponse(
                response=inline_serializer(
                    name="Not Found",
                    fields={"detail": serializers.CharField()},
                )
            ),
            400: OpenApiResponse(
                response=inline_serializer(
                    name="Error input data",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
    def put(self, request, *args, **kwargs):
        mailing_id = request.GET.get("id")

        instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        serializer = MailingSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=MailingSerializer,
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='Description of the query parameter',
                required=True,
            ),
        ],
        responses={
            204: OpenApiResponse(),
            404: OpenApiResponse(
                response=inline_serializer(
                    name="Not Found",
                    fields={"detail": serializers.CharField()},
                )
            )
        }
    )
    def delete(self, request, format=None):
        mailing_id = request.GET.get("id")

        instance = get_object_or_404(klass=MailingModel, pk=mailing_id)

        task = CeleryTaskModel.objects.get(mailing=instance)

        current_app.control.revoke(task.task_id, terminate=True)

        instance.delete()
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
