from django import forms
from .models import TwitterUserSearched
from django.core.exceptions import ValidationError


class TwitterUsernameForm(forms.ModelForm):
    class Meta:
        model = TwitterUserSearched
        fields = [
            "twitter_username",
        ]
        labels = [""]

    def clean_twitterusername(self):
        exclude_list = [
            "franciscojarceo",
            "mlevchin",
            "affirm",
        ]
        cleaned_data = super(TwitterUsernameForm, self).clean()
        data = cleaned_data.get("twitter_username")
        if data in exclude_list:
            raise ValidationError("sorry that's not allowed!")
        return data
