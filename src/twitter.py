import tweepy
import os
from configparser import SectionProxy
from typing import Iterable, Dict
from src.tables import Tweet
from sqlalchemy.orm.attributes import InstrumentedAttribute


def api_auth(consumer_key: str, consumer_secret: str, access_token: str, access_key: str) -> tweepy.API:

    # Setup tweepy to authenticate with Twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_key)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api


def fetch_tweets(user: str, n: int, cfg: SectionProxy) -> Iterable[Dict]:

    api = api_auth(os.environ.get('consumer_key') or cfg['consumer_key'],
                   os.environ.get('consumer_secret') or cfg['consumer_secret'],
                   os.environ.get('access_token') or cfg['access_token'],
                   os.environ.get('access_key') or cfg['access_key'])

    # Filter out all columns which aren't in our Tweet model
    cols = [k for k, v in Tweet.__dict__.items() if isinstance(v, InstrumentedAttribute)]

    # Get a particular user's timeline (up to N of his/her most recent tweets)
    for t in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode='extended').items(n):
        yield {k: v for k, v in t._json.items() if k in cols}
