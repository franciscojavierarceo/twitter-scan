from django import forms
from .models import TwitterUserSearched


class TwitterUsernameForm(forms.ModelForm):
    class Meta:
        model = TwitterUserSearched
        fields = [
            "twitter_username",
        ]
        labels = [""]
