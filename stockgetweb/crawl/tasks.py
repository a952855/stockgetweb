# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model

from celery import Celery, shared_task

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['stockgetweb.crawl.tasks'])


@shared_task
def my_name(name):

    user = get_user_model().objects.create_user(
        username=f'{name}', password=f'{name}', email='test@admin.com.tw')
