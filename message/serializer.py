from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    sending_time = serializers.DateTimeField()

    status = serializers.CharField()

    mailing_id = serializers.IntegerField()

    client_id = serializers.IntegerField()