from django.contrib import admin
from .models import TwitterAuthToken, TwitterUser, TwitterUserSearched, Tweet


admin.site.register(TwitterUserSearched)
admin.site.register(TwitterAuthToken)
admin.site.register(TwitterUser)
admin.site.register(Tweet)
