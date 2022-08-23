from django import forms
from crispy_forms.helper import FormHelper
from .models import TwitterUserSearched
from django.core.exceptions import ValidationError


class TwitterUsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TwitterUsernameForm, self).__init__(*args, **kwargs)
        self.fields["twitter_username"].label = False

    class Meta:
        model = TwitterUserSearched
        fields = [
            "twitter_username",
        ]
        labels = [""]

    def clean_twitter_username(self):
        exclude_list = [
            "franciscojarceo",
            "mlevchin",
            "affirm",
        ]
        data = self.cleaned_data.get("twitter_username")
        data = data.replace("@", "").lower().strip()
        if data in exclude_list:
            raise ValidationError("sorry that's not allowed!")
        return data

    def clean(self):
        cleaned_data = super().clean()
        twitter_username = cleaned_data.get("twitter_username")

        return cleaned_data
