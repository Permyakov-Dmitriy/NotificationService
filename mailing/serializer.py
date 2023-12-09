from rest_framework import serializers, fields

from .utils.task import create_task
from .utils.format_date import string_to_arrays_int
from .models import CeleryTaskModel

from datetime import datetime
from celery import current_app


class MailingSerializer(serializers.Serializer):
    launch_time = serializers.DateTimeField()

    finish_time = serializers.DateTimeField()

    message_text = serializers.CharField()

    filter_tags = serializers.ListField(child=serializers.IntegerField(), default=None)

    filter_operator = serializers.IntegerField()

    def update(self, instance, validated_data):
        task = CeleryTaskModel.objects.get(mailing=instance)

        instance.launch_time = validated_data.get('launch_time', instance.launch_time)
        instance.finish_time = validated_data.get('finish_time', instance.finish_time)
        instance.message_text = validated_data.get('message_text', instance.message_text)
        instance.filter_tags = validated_data.get('filter_tags', instance.filter_tags)
        instance.filter_operator = validated_data.get('filter_operator', instance.filter_operator)

        current_app.control.revoke(task.task_id, terminate=True)

        task.delete()

        arr_date_time, time_zone = string_to_arrays_int(str(instance.launch_time))

        time_diff = datetime(*arr_date_time) - datetime.now()

        create_task(instance, time_diff, time_zone)

        instance.save()

        return instance


class StatisticsSerializer(serializers.Serializer):
    mailing = MailingSerializer()

    messages = serializers.JSONField(default=None)