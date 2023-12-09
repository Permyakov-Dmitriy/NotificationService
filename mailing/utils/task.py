from ..models import CeleryTaskModel

from celery import current_app
from datetime import datetime, timedelta


def create_task(mailing_instance, time_diff, time_zone):
    task = current_app.send_task('mailing.tasks.mailing_task', args=[mailing_instance.id],
        eta=datetime.now() + time_diff - timedelta(hours=time_zone[0], minutes=time_zone[1])
    )

    task_instance = CeleryTaskModel.objects.create(
        mailing=mailing_instance,
        task_id=task.id
    )

    return task_instance