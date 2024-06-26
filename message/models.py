from django.db import models

from client.models import ClientModel
from mailing.models import MailingModel


class MessageModel(models.Model):
    sending_time = models.DateTimeField()

    status = models.CharField(max_length=50)

    mailing_id = models.ForeignKey(MailingModel, related_name="msg_mail", on_delete=models.CASCADE)

    client_id = models.ForeignKey(ClientModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mailing_id} {self.client_id.phone_number} {self.status}'
    