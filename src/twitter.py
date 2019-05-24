import tweepy
import os
from configparser import SectionProxy
from typing import Iterable, Dict
from src.tables import Tweet
from sqlalchemy.orm.attributes import InstrumentedAttribute


def api_auth(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> tweepy.API:

    """
    Handles Twitter API OAuth authentication and generates tweepy API object.
    API object is instantiated with compression and automatic wait on rate limit
    settings

    :param consumer_key: Twitter API consumer key string
    :param consumer_secret: Twitter API consumer secret string
    :param access_token: Twitter API access token string
    :param access_token_secret: Twitter API access key string
    :return: Tweepy API object
    """

    # Setup tweepy to authenticate with Twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api


def fetch_tweets(user: str, n: int, cfg: SectionProxy) -> Iterable[Dict]:

    """
    Fetches N last tweets for the specified user (hard limit of 3200 tweets)

    :param user: Twitter username to fetch tweets from
    :param n: Number of tweets to fetch
    :param cfg: "twitter" section of the config
    :return: generator containing all tweets fetched
    """

    api = api_auth(os.environ.get('consumer_key') or cfg['consumer_key'],
                   os.environ.get('consumer_secret') or cfg['consumer_secret'],
                   os.environ.get('access_token') or cfg['access_token'],
                   os.environ.get('access_token_secret') or cfg['access_token_secret'])

    # Filter out all columns which aren't in our Tweet model
    cols = [k for k, v in Tweet.__dict__.items() if isinstance(v, InstrumentedAttribute)]

    # Get a particular user's timeline (up to N of his/her most recent tweets)
    for t in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode='extended').items(n):
        yield {k: v for k, v in t._json.items() if k in cols}
