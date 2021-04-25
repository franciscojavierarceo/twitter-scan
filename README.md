# twitter-scan

This is a repository hosting a small project idea from Twitter.

These are the goals of this project:

1. Learn Fast-API
2. Learn Twitter's Oauth2 for Fast-API
3. Deploy an NLP model using word embeddings
4. Have the model auto-update based on feedback (this is a maybe and I'd probably schedule it)
5. Deploy the application on Docker Swarm

# Building Locally

As a first step, you need to generate a environment file located `./twitter-scan/.env`, the subfolder in this repository. It will look like:

```.env
DOMAIN=localhost
# DOMAIN=local.dockertoolbox.tiangolo.com
# DOMAIN=localhost.tiangolo.com
# DOMAIN=dev.domain.com

STACK_NAME=domain-com

TRAEFIK_PUBLIC_NETWORK=traefik-public
TRAEFIK_TAG=domain.com
TRAEFIK_PUBLIC_TAG=traefik-public

DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_CELERYWORKER=celeryworker
DOCKER_IMAGE_FRONTEND=frontend

# Backend
BACKEND_CORS_ORIGINS=["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", "https://localhost", "https://localhost:4200", "https://localhost:3000", "https://localhost:8080", "http://dev.domain.com", "https://stag.domain.com", "https://domain.com", "http://local.dockertoolbox.tiangolo.com", "http://localhost.tiangolo.com"]
PROJECT_NAME=twitter-scan
SECRET_KEY=
FIRST_SUPERUSER=admin@domain.com
FIRST_SUPERUSER_PASSWORD=
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=
SMTP_USER=admin
SMTP_PASSWORD=
EMAILS_FROM_EMAIL=info@domain.com

USERS_OPEN_REGISTRATION=False

SENTRY_DSN=

# Flower
FLOWER_BASIC_AUTH=

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=
POSTGRES_DB=app

# PgAdmin
PGADMIN_LISTEN_PORT=5050
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=

TWITTER_API_KEY=
TWITTER_API_SECRET=
```

To build this repository locally cd into the subfolder `twitter-scan` that was built from Fast's cookiecutter template, then simply run:

```
cd twitter-scan/
docker-compose up --build
```

After the container is built you can then just run the line below to have the serve run as a background task.
```
docker-compose up -d
```

# Notebook Demo

To see how this behaves in a simple Jupyter Notebook open `Twitter-Mining.ipynb` and examine the behavior there. You'll need your twitter developer credentials to do this.
