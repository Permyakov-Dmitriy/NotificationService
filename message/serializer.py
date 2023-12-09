from rest_framework import serializers

from client.serializer import ClientSerializer
from mailing.serializer import MailingSerializer


class MessageSerializer(serializers.Serializer):
    sending_time = serializers.DateTimeField()

    status = serializers.CharField()

    mailing_id = MailingSerializer(read_only=True)

    client_id = ClientSerializer(read_only=True)