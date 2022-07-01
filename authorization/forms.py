from django import forms


class TwitterUsernameForm(forms.Form):
    twitter_username = forms.CharField(label='Twitter Username', max_length=20, required=False)