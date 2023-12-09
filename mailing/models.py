from django.db import models
from django.contrib.postgres import fields


class MailingModel(models.Model):
    launch_time = models.DateTimeField()    

    finish_time = models.DateTimeField()

    message_text = models.TextField()

    filter_tags = fields.ArrayField(models.IntegerField(), default=None, null=True)

    filter_operator = models.IntegerField(default=None, null=True)

    def __str__(self):
        return f'{self.message_text} {self.filter_tags} {self.filter_operator}'


class CeleryTaskModel(models.Model):
    mailing = models.ForeignKey(MailingModel, related_name="mailing", on_delete=models.CASCADE)

    task_id = models.CharField()
