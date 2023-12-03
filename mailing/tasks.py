# tasks.py
from celery import shared_task
from datetime import datetime, timedelta

@shared_task
def your_task():
    print('\nHello!\n')
