from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import LinkTagAndClientModel
from .utils.link_tags import create_link_tags


class ClientSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    timezone = serializers.CharField(max_length=63)

    tags = serializers.ListField(default=None)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.timezone = validated_data.get('timezone', instance.timezone)

        phone_number_str = str(instance.phone_number)

        instance.operator_code = phone_number_str[1:4]

        instance.save()

        tags = validated_data.get('tags', None)

        if tags:
            LinkTagAndClientModel.objects.filter(client=instance).delete()

            create_link_tags(instance, tags)

        return instance