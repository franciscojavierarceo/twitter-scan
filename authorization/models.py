from re import I
from django.db import models


class TwitterAuthToken(models.Model):
    oauth_token = models.CharField(max_length=255)
    oauth_token_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.oauth_token


class TwitterUser(models.Model):
    twitter_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_image_url = models.CharField(max_length=255, null=True)
    twitter_oauth_token = models.ForeignKey(TwitterAuthToken, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.screen_name


class TwitterUserSearched(models.Model):
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)
    twitter_username = models.CharField(max_length=255)
    submitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.twitter_username} - {self.submitter_user}"


class Tweet(models.Model):
    tweet_id = models.BigIntegerField(null=True)
    created_date = models.DateTimeField(null=True)
    tweet_date = models.DateTimeField(null=True)
    twitter_username = models.CharField(max_length=255)
    tweet_text = models.CharField(max_length=500, null=True)
    toxicity_score = models.FloatField(null=True)

    def __str__(self):
        return f"{self.twitter_username} - {self.tweet_id}"
