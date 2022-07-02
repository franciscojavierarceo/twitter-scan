import os
import re
import tweepy
import pandas as pd
from detoxify import Detoxify

TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
api = tweepy.API(auth)


def get_all_tweets(screen_name: str) -> list:
    # initialize a list to hold all the tweepy Tweets
    alltweets = []  

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200, max_id=oldest)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")

    return alltweets

def clean_tweet(x: str) -> str:
    try:
        clean = re.sub("@[A-Za-z0-9_]+","", x).strip()
        replytweet = re.match('… https://t.co/*', clean)
        if replytweet is not None:
            if replytweet.end() > 0:
                return None
        return clean
    except Exception as e:
        print(e)
        return x