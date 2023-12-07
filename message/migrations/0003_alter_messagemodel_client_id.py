# Generated by Django 4.2.7 on 2023-12-06 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_linktagandclientmodel_client'),
        ('message', '0002_alter_messagemodel_mailing_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientmodel'),
        ),
    ]