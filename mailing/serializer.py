from rest_framework import serializers, fields


class MailingSerializer(serializers.Serializer):
    launch_time = serializers.DateTimeField()

    finish_time = serializers.DateTimeField()

    message_text = serializers.CharField()

    filter_tags = serializers.ListField(child=serializers.IntegerField(), default=None)

    filter_operator = serializers.IntegerField()


class StatisticsSerializer(serializers.Serializer):
    mailing = MailingSerializer()
    messages = serializers.JSONField(default=None)