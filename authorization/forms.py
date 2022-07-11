from django import forms
from crispy_forms.helper import FormHelper
from .models import TwitterUserSearched
from django.core.exceptions import ValidationError


class TwitterUsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TwitterUsernameForm, self).__init__(*args, **kwargs)
        self.fields['twitter_username'].label = False

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
