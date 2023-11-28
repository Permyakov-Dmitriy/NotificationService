from rest_framework import serializers


class MailingSerializer(serializers.Serializer):
    launch_time = serializers.DateTimeField()

    finish_time = serializers.DateTimeField()

    message_text = serializers.CharField()

    filter_properties = serializers.CharField(max_length=50)