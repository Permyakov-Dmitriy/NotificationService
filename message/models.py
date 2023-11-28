from django.db import models

from client.models import ClientModel
from mailing.models import MailingModel


class MessageModel(models.Model):
    sending_time = models.DateTimeField()

    status = models.CharField(max_length=50)

    mailing_id = models.ForeignKey(MailingModel, related_name="mailing_id", on_delete=models.CASCADE)

    client_id = models.ForeignKey(ClientModel, related_name="client_id", on_delete=models.CASCADE)
