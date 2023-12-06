from django.db.models import Q

from client.models import ClientModel
from mailing.models import MailingModel

from celery import shared_task
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
import asyncio
import aiohttp


@sync_to_async
def get_mailing(mailing_id):
    return MailingModel.objects.get(id=mailing_id)

@sync_to_async
def get_users(mailing):
    return ClientModel.objects.filter(
        Q(client__tag_id__in=mailing.filter_tags) |
        Q(operator_code=mailing.filter_operator)
    ).distinct()

async def fetch_data(session, url, headers, data):
    async with session.post(url, headers=headers, json=data) as response:
        if response.status == 200:
            return await response.text()
        return 'Error'
    
async def main(users, mailing):
    api_url = "https://probe.fbrq.cloud/v1/send/"

    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        '.eyJleHAiOjE3MzI2MzMzMDcsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9EbWl0cml5R2lib24ifQ'
        '.Y4CmrhFLweZ8as_rhm4q3IaNHJPx4BQHjn3Os0F9OH8'
    }

    async with aiohttp.ClientSession() as session:
        tasks = []

        for user in users:
            payload = {
                'id': user.id,
                "phone": int(user.operator_code[1:]),
                "text": mailing.message_text
            }

            task = asyncio.create_task(fetch_data(session, api_url + str(user.id), headers, payload))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

    for res in results:
        print(res)

@shared_task
async def your_task(mailing_id):
    mailing = await get_mailing(mailing_id)
    users = await get_users(mailing)

    await main(users, mailing)
