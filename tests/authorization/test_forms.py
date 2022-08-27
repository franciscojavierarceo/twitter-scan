from http import HTTPStatus

from django.test import TestCase
from authorization.forms import TwitterUsernameForm


class SearchTwitterUserFormTests(TestCase):
    def test_submit_valid_username(self):
        form = TwitterUsernameForm(data={"twitter_username": "twitter"})
        self.assertEqual(form.errors, {})

    def test_submit_invalid_username(self):
        form = TwitterUsernameForm(data={"twitter_username": "franciscojarceo"})
        self.assertEqual(
            form.errors, {"twitter_username": ["sorry that's not allowed!"]}
        )

    def test_post_form_submission_cleanup(self):
        testcases = [
            " @ twitter ",
            "@twitter",
            "@TWITTER",
            " @ TWITTER ",
        ]
        for testcase in testcases:
            form = TwitterUsernameForm(data={"twitter_username": testcase})
            form.save()
            self.assertEqual(form.cleaned_data["twitter_username"], "twitter")
