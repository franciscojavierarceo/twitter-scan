# Render App

To run the poetry to get this started simply run:

```commandline
poetry install
```

If you have issues with your shell just run:
```commandline
poetry env use python3.7
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