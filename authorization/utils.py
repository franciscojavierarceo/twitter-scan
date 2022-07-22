import os
import re
from datetime import datetime

import pytz
import tweepy
from asgiref.sync import async_to_sync
from celery import shared_task
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone

from authorization.load_model import Detoxify
from authorization.models import Tweet

model = Detoxify("original-small")
test_pred = model.predict("this is running the model at buildtime")
print(f"running build-time prediction: {test_pred}")

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
twitter_api = tweepy.API(auth)


def get_score_save_historical_tweets(screen_name: str, n_tweets: int = 20) -> None:
    print(f"getting historical tweets for {screen_name}...")

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = twitter_api.user_timeline(screen_name=screen_name, count=n_tweets)
    tweet_counter: int = len(new_tweets)

    print(f"retrieved {tweet_counter} tweets for {screen_name}...")
    # keep grabbing tweets until there are no tweets left to grab

    while len(new_tweets) > 0:
        print(f"getting tweets before {new_tweets[-1].created_at}")
        # save the id of the oldest tweet less one
        oldest = new_tweets[-1].id - 1

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = twitter_api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest
        )
        tweet_counter += len(new_tweets)
        # save most recent tweets
        tweets = clean_tweets(new_tweets)
        score_and_save_tweets(screen_name, tweets)

        print(f"...{tweet_counter} tweets downloaded so far")
    print("finished getting historical tweets")


def get_tweets(screen_name: str, n_tweets: int = 20) -> list:
    print(f"getting tweets for {screen_name}...")

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = twitter_api.user_timeline(screen_name=screen_name, count=n_tweets)
    tweet_counter = len(new_tweets)
    print(f"retrieved {tweet_counter} tweets for {screen_name}...")

    return new_tweets


def clean_tweet(x: str) -> str:
    try:
        clean = re.sub("@[A-Za-z0-9_]+", "", x).strip()
        reply_tweet = re.match("… https://t.co/*", clean)
        if reply_tweet is not None:
            if reply_tweet.end() > 0:
                return None
        return clean
    except Exception as e:
        print(f"failed to clean tweet {e}")
        return x


def clean_tweets(tweets: list) -> list:
    print("cleaning all tweets...")
    res = []
    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet._json["text"])
        res.append(
            (
                tweet._json["id"],
                tweet._json["created_at"],
                tweet._json["text"],
                cleaned_tweet,
            )
        )
    return res


def score_tweets(input_text: str) -> float:
    preds = model.predict(input_text)
    return preds["toxicity"]


@transaction.atomic
def score_and_save_tweets(screen_name: str, tweets: list) -> None:
    print(f"scoring all {len(tweets)} tweets for {screen_name}...")
    tweet_text = [j[3] if j[3] else "" for j in tweets]
    tweet_scores = score_tweets(tweet_text)
    print(f"saving all tweets for {screen_name}...")
    for tweet, tweet_score in zip(tweets, tweet_scores):
        tweet_date = datetime.strptime(
            tweet[1], "%a %b %d %H:%M:%S +0000 %Y"
        ).astimezone(pytz.UTC)
        db_tweet = Tweet(
            created_date=timezone.now(),
            tweet_id=tweet[0],
            twitter_username=screen_name,
            tweet_text=tweet[2],
            tweet_date=tweet_date,
            toxicity_score=round(tweet_score * 100.0, 2),
        )
        db_tweet.save()
    print('...scoring complete')


@async_to_sync
async def fetch_and_store_tweets(screen_name: str) -> HttpResponse:
    response = HttpResponse()
    try:
        tweets = get_tweets(screen_name)
        tweets = clean_tweets(tweets)
        score_and_save_tweets(screen_name, tweets)
        response["status_code"] = 200
    except Exception as e:
        print(f"failed to store tweets {e}")
        response["status_code"] = 500

    return response


@shared_task
def fetch_and_store_historical_tweets(screen_name: str) -> None:
    try:
        get_score_save_historical_tweets(screen_name, n_tweets=200)
    except Exception as e:
        print(f"failed to get historical tweets: {e}")

    return None
