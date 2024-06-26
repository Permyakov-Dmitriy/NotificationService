# Generated by Django 4.2.7 on 2023-11-29 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='clientmodel',
            name='tag',
        ),
        migrations.CreateModel(
            name='LinkTagAndClientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='client.clientmodel')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='client.tagmodel')),
            ],
        ),
    ]
