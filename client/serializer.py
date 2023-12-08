from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class ClientSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    timezone = serializers.CharField(max_length=63)

    tags = serializers.ListField(default=None)
