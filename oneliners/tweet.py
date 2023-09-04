# a simple module to tweet a message, using configuration from settings
#
# To access twitter via OAuth, you need to first obtain:
# consumer key, consumer secret, access token, access token secret
#
# 1. Login to Twitter
# 2. Go to https://dev.twitter.com/apps/new and fill the form
#    - Application Type should be Client
#    - Default Access Type must be Read and Write
# 3. Consumer key and secret are here: https://dev.twitter.com/apps
# 4. Access token and secret are in the My Access Token menu
#

from logging import getLogger

from django.conf import settings

import tweepy

TWITTER_CREDENTIAL_KEYS = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')
TWEET_LENGTH_LIMIT = 280

logger = getLogger(__name__)


def get_validated_twitter_credentials():
    twitter_settings = settings.TWITTER
    have_creds = True
    for key in TWITTER_CREDENTIAL_KEYS:
        if key not in twitter_settings or not twitter_settings[key]:
            have_creds = False
            logger.warning('settings.TWITTER[%s] is missing. Will not be able to authenticate to Twitter.', key)

    return twitter_settings if have_creds else None


def send_tweet(message, test=False):
    creds = get_validated_twitter_credentials()

    if not creds:
        logger.error('Cannot tweet because settings.TWITTER is incomplete.')
        return False

    # https://docs.tweepy.org/en/v4.14.0/examples.html
    api = tweepy.Client(
        consumer_key=creds['consumer_key'],
        consumer_secret=creds['consumer_secret'],
        access_token=creds['access_token'],
        access_token_secret=creds['access_token_secret'],
    )

    if test:
        logger.info(message)
        return True

    try:
        return api.create_tweet(text=message)
    except tweepy.errors.TweepyException as e:
        logger.error('Tweepy error: %s', e)


def format_message(summary, line, url):
    def with_hashtags(s):
        for hashtag in '#bash', '#linux':
            s2 = s + ' ' + hashtag
            if len(s2) <= TWEET_LENGTH_LIMIT:
                s = s2
            else:
                break

        return s

    message = with_hashtags('{}: {}; {}'.format(summary, line, url))
    if len(message) <= TWEET_LENGTH_LIMIT:
        return message

    message = with_hashtags('{}; {}'.format(line, url))
    if len(message) <= TWEET_LENGTH_LIMIT:
        return message

    return '{}; {}'.format(ellipsize(line, TWEET_LENGTH_LIMIT - len(url) - 2), url)


def ellipsize(s, maxlen):
    if len(s) <= maxlen:
        return s

    return '{}...'.format(s[:maxlen-3])
