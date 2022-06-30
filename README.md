# Render App

To run the poetry to get this started simply run:

```
poetry install
```

If you have issues with your shell just run:
```
poetry env use python3.7
```

To properly start the app simply run:

```
poetry shell
export $(xargs < .env)
python manage.py runserver
```