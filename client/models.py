from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class TagModel(models.Model):
    mark = models.CharField(max_length=50)

    def __str__(self):
        return self.mark


class ClientModel(models.Model):
    phone_number = PhoneNumberField()

    operator_code = models.IntegerField(default=None)

    timezone = models.CharField(max_length=63)

    def __str__(self):
        return f'{self.phone_number} {self.timezone}'


class LinkTagAndClientModel(models.Model):
    tag = models.ForeignKey(TagModel, related_name="tag", on_delete=models.CASCADE)

    client = models.ForeignKey(ClientModel, related_name="client", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client.phone_number} {self.tag}'