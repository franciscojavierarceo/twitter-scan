from django.db import models

# Create your models here.
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
