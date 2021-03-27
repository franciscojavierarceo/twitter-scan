# twitter-scan

This is a repository hosting a small project idea from Twitter.

These are the goals of this project:

1. Learn Fast-API
2. Learn Twitter's Oauth2 for Fast-API
3. Deploy an NLP model using word embeddings
4. Have the model auto-update based on feedback (this is a maybe and I'd probably schedule it)
5. Deploy the application on Docker Swarm

# Building Locally

To build this repository locally cd into the subfolder `twitter-scan` that was built from Fast's cookiecutter template, then simply run:

```
docker-compose up --build
```

After the container is built you can then just run the line below to have the serve run as a background task.
```
docker-compose up -d
```
