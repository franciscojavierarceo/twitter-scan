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


    def clean(self):
        cleaned_data = super(TwitterUsernameForm, self).clean()
        data = self.cleaned_data['twitter_username']
        #if "franciscojarceo" in data:
        if True:
            raise ValidationError("sorry bro not frannie!")
        return data
