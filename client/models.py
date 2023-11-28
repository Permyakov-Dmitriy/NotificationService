from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ClientModel(models.Model):
    phone_number = PhoneNumberField()

    operator_code = models.CharField(max_length=3)

    tag = models.CharField(max_length=50)

    timezone = models.CharField(max_length=63)
