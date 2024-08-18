# Toxic Twitter Scanner

This repository is a web app that allows you to scan a 
user's tweets to see how "toxi" they are according to an open source model.

I [wrote about it in more detail here](https://www.chaos-engineering.dev/p/building-an-ai-to-scan-toxic-tweets).

# Render App

To run the poetry to get this started simply run:

```commandline
poetry install
```

If you have issues with your shell just run:
```commandline
poetry env use python3.7
```

# Getting Started

You'll need to add a .env file with the following keys:
```
SECRET_KEY=
ALLOWED_HOSTS=127.0.0.1,localhost,YOUR_DOMAIN_NAME
TWITTER_OAUTH_CALLBACK_URL=http://127.0.0.1:8000/twitter_callback/
TWITTER_API_KEY_OLD=
TWITTER_API_SECRET_OLD=
TWITTER_CLIENT_ID_OLD=
TWITTER_CLIENT_SECRET_OLD=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_API_BEARER_TOKEN=
TWITTER_CLIENT_ID=
TWITTER_CLIENT_SECRET=
SERVER_EMAIL=
CELERY_BROKER_URL=redis://@localhost
INTERNAL_MODEL_ENDPOINT=http://localhost:8000/score-tweets/
DJANGO_SETTINGS_MODULE=tweetscanner.settings

```
To properly start the app simply run:

```commandline
poetry shell
export $(xargs < .env)
python manage.py runserver
```

# Celery

To launch the celery worker simply open up another terminal and run
```commandline
celery -A tweetscanner worker -l info
```


