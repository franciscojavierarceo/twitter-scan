from curses.ascii import HT
import os
import re
import tweepy
import pytz
from django.utils import timezone
from datetime import datetime

from django.http import HttpResponse
from authorization.load_model import Detoxify
from authorization.models import Tweet
from django.db import transaction

model = Detoxify("original-small")
testpred = model.predict("this is running the model at buildtime")
print(f"running buildtime prediction: {testpred}")

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
# auth = tweepy.OAuth2BearerHandler(os.environ.get("TWITTER_API_BEARER_TOKEN"))
api = tweepy.API(auth)


def get_tweets(screen_name: str, ntweets=20, get_historical=False) -> list:
    print(f"getting all tweets for {screen_name}...")
    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=ntweets)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    if get_historical:
        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print(f"getting tweets before {oldest}")
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=screen_name, count=200, max_id=oldest
            )
            # save most recent tweets
            alltweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print(f"...{len(alltweets)} tweets downloaded so far")

    return alltweets


def clean_tweet(x: str) -> str:
    try:
        clean = re.sub("@[A-Za-z0-9_]+", "", x).strip()
        replytweet = re.match("… https://t.co/*", clean)
        if replytweet is not None:
            if replytweet.end() > 0:
                return None
        return clean
    except Exception as e:
        print(e)
        return x


def clean_tweets(tweets: list) -> list:
    print("cleaning all tweets...")
    res = []
    for i in tweets:
        if i._json["in_reply_to_status_id"] is not None:
            cleaned = clean_tweet(i._json["text"])
            res.append(
                (
                    i._json["id"],
                    i._json["created_at"],
                    i._json["text"],
                    cleaned,
                )
            )
    return res


def score_tweets(input_text: str) -> float:
    preds = model.predict(input_text)
    return preds["toxicity"]


@transaction.atomic
def score_and_save_tweets(screen_name: str, tweets: list) -> None:
    print(f"scoring all tweets for {screen_name}...")
    tweettext = [j[3] if j[3] else "" for j in tweets]
    tweet_scores = score_tweets(tweettext)
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


def fetch_and_store_tweets(screen_name: str) -> HttpResponse:
    response = HttpResponse()
    try:
        tweets = get_tweets(screen_name)
        tweets = clean_tweets(tweets)
        score_and_save_tweets(screen_name, tweets)
        response["status_code"] = 200
    except Exception as e:
        print(e)
        response["status_code"] = 500

    return response
