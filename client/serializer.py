from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class ClientSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    operator_code = serializers.CharField(max_length=3)

    tags = serializers.CharField(default=None)

    timezone = serializers.CharField(max_length=63)