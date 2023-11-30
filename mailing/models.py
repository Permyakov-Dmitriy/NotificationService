from django.db import models


class MailingModel(models.Model):
    launch_time = models.DateTimeField()

    finish_time = models.DateTimeField()

    message_text = models.TextField()

    filter_properties = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.message_text} {self.filter_properties}'
