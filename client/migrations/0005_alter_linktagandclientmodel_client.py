# Generated by Django 4.2.7 on 2023-12-06 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_linktagandclientmodel_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linktagandclientmodel',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='client.clientmodel'),
        ),
    ]