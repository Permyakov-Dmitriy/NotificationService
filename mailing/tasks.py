from django.db.models import Q

from client.models import ClientModel
from mailing.models import MailingModel
from message.models import MessageModel

from celery import shared_task
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
import asyncio
import aiohttp


@sync_to_async
def create_message(status, mailing_id, client_id):
    formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    MessageModel.objects.create(
        sending_time=formatted_now,
        status=status,
        mailing_id=mailing_id,
        client_id=client_id
    )


@sync_to_async
def get_mailing(mailing_id):
    return MailingModel.objects.get(id=mailing_id)


@sync_to_async
def get_users(filter_tags, filter_operator):
    return list(ClientModel.objects.filter(
        Q(client__tag_id__in=filter_tags) |
        Q(operator_code=filter_operator)
    ).distinct())


async def fetch_data(session, url, headers, data, mailing_id, user_id):
    async with session.post(url, headers=headers, json=data) as response:
        if response.status == 200:
            res_txt = await response.text()

            if res_txt == '{"code":0,"message":"OK"}':
                await create_message('Delivered', mailing_id, user_id)
        else:
            await create_message('Failed', mailing_id, user_id)

        print(f'{url} status:{response.status}')
    

async def main(mailing_id):
    mailing = await get_mailing(mailing_id)
    try:
        users = await get_users(mailing.filter_tags, mailing.filter_operator)
    except TypeError:
        return 0

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
                "id": user.id,
                "phone": int(str(user.phone_number)[1:]),
                "text": mailing.message_text
            }

            task = asyncio.create_task(fetch_data(session, api_url + str(user.id), headers, payload, mailing, user))
            tasks.append(task)

        results = await asyncio.gather(*tasks)


@shared_task
def your_task(mailing_id):
    asyncio.run(main(mailing_id))
