from django.db import models


class MailingModel(models.Model):
    launch_time = models.DateTimeField()

    finish_time = models.DateTimeField()

    message_text = models.TextField()

    filter_properties = models.CharField(max_length=50)
