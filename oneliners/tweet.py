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

logger = getLogger(__name__)


def get_validated_twitter_credentials():
    twitter_settings = settings.TWITTER
    have_creds = True
    for key in TWITTER_CREDENTIAL_KEYS:
        if key not in twitter_settings or not twitter_settings[key]:
            have_creds = False
            logger.warning('settings.TWITTER[%s] is missing. Will not be able to authenticate to Twitter.', key)

    return twitter_settings if have_creds else None


def tweet(message, test=False):
    logger.debug(message)

    creds = get_validated_twitter_credentials()

    if not creds:
        logger.error('Cannot tweet because settings.TWITTER is incomplete.')
        return False

    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])
    api = tweepy.API(auth)

    # shorten the text to make room for #bash
    if len(message) > 134:
        message = message[:130] + ' ...'
    message += ' #bash'

    # if there is still room for #linux, append it
    if len(message) < 134:
        message += ' #linux'

    if test:
        logger.info(message)
        return True

    try:
        return api.update_status(message)
    except tweepy.error.TweepError as e:
        logger.error('TweepError: %s', e)
