import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import twitter_login_required
from .models import Tweet, TwitterAuthToken, TwitterUser, TwitterUserSearched
from .authorization import create_update_user_from_twitter, check_token_still_valid
from twitter_api.twitter_api import TwitterAPI
from .forms import TwitterUsernameForm
from .utils import fetch_and_store_tweets
from django.http import HttpResponseRedirect
from django.utils import timezone


def twitter_login(request):
    print("calling twitter api")
    try:
        twitter_api = TwitterAPI()
        url, oauth_token, oauth_token_secret = twitter_api.twitter_login()
        if url is None or url == "":
            messages.add_message(
                request, messages.ERROR, "Unable to login. Please try again."
            )
            return render(request, "authorization/error_page.html")
        else:
            twitter_auth_token = TwitterAuthToken.objects.filter(
                oauth_token=oauth_token
            ).first()
            if twitter_auth_token is None:
                twitter_auth_token = TwitterAuthToken(
                    oauth_token=oauth_token, oauth_token_secret=oauth_token_secret
                )
                twitter_auth_token.save()
            else:
                twitter_auth_token.oauth_token_secret = oauth_token_secret
                twitter_auth_token.save()

            print(f"redirecting to {url}")
            return redirect(url)
    except Exception as e:
        print(f"failed to attempt login:\n{e}")
        return render(request, "authorization/index.html")


def twitter_callback(request):
    if "denied" in request.GET:
        messages.add_message(
            request,
            messages.ERROR,
            "Unable to login or login canceled. Please try again.",
        )
        return render(request, "authorization/error_page.html")
    twitter_api = TwitterAPI()
    oauth_verifier = request.GET.get("oauth_verifier")
    oauth_token = request.GET.get("oauth_token")
    twitter_auth_token = TwitterAuthToken.objects.filter(
        oauth_token=oauth_token
    ).first()
    if twitter_auth_token is not None:
        access_token, access_token_secret = twitter_api.twitter_callback(
            oauth_verifier, oauth_token, twitter_auth_token.oauth_token_secret
        )
        if access_token is not None and access_token_secret is not None:
            twitter_auth_token.oauth_token = access_token
            twitter_auth_token.oauth_token_secret = access_token_secret
            twitter_auth_token.save()
            # Create user
            info = twitter_api.get_me(access_token, access_token_secret)
            if info is not None:
                twitter_user_new = TwitterUser(
                    twitter_id=info[0]["id"],
                    screen_name=info[0]["username"],
                    name=info[0]["name"],
                    profile_image_url=info[0]["profile_image_url"],
                )
                twitter_user_new.twitter_oauth_token = twitter_auth_token
                user, twitter_user = create_update_user_from_twitter(twitter_user_new)
                if user is not None:
                    login(request, user)
                    return redirect("index")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Unable to get profile details. Please try again.",
                )
                return render(request, "authorization/error_page.html")
        else:
            messages.add_message(
                request, messages.ERROR, "Unable to get access token. Please try again."
            )
            return render(request, "authorization/error_page.html")
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "Unable to retrieve access token. Please try again.",
        )
        return render(request, "authorization/error_page.html")

@login_required
@twitter_login_required
def index(request):
    if request.method == "POST":
        form = TwitterUsernameForm(request.POST)
        print(f"form valid = {form.is_valid()}")
        dtz = timezone.now()
        curr_user = TwitterUser.objects.get(user=request.user)
        tuser = request.POST.get("twitter_username", None)
        db_recs = TwitterUserSearched.objects.filter(
            twitter_username=tuser,
            submitter_user=curr_user,
        )
        if form.is_valid():
            if db_recs.count() > 0:
                print(f"{db_recs.count()} records found")
                db_rec = db_recs.last()
                db_rec.updated_date = dtz
                db_rec.save()
                return redirect("results")
            else:
                print("no records found")
                model_saved = form.save()
                model_saved.submitter_user = curr_user
                model_saved.created_date = dtz
                model_saved.updated_date = dtz
                model_saved.save()
                print(fetch_and_store_tweets(tuser))
                return redirect("results")
    else:
        form = TwitterUsernameForm()

    return render(request, "authorization/index.html", {"form": form})


@login_required
def twitter_logout(request):
    logout(request)
    return redirect("index")

@login_required
def results(request):
    curr_user = TwitterUser.objects.get(user=request.user)
    results = TwitterUserSearched.objects.filter(
        submitter_user=curr_user,
    )

    tweets = Tweet.objects.filter(
        twitter_username__in=results.values_list("twitter_username", flat=True)
    ).order_by("twitter_username", "-toxicity_score")
    
    return render(
        request, "authorization/results.html", {"results": results, "tweets": tweets}
    )
