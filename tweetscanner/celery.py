from __future__ import absolute_import
import os
import django

# from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tweetscanner.settings")
app = Celery("tweetscanner", broker=os.getenv("CELERY_BROKER_URL"))
django.setup()

from django.conf import settings
from authorization.utils import fetch_and_store_tweets


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def twitter_scrape_task(screen_name: str):
    print(fetch_and_store_tweets(screen_name=screen_name))

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
