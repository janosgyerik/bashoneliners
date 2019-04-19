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


logger = getLogger(__name__)

have_creds = False
try:
    consumer_key = settings.TWITTER['consumer_key']
    consumer_secret = settings.TWITTER['consumer_secret']
    access_token = settings.TWITTER['access_token']
    access_token_secret = settings.TWITTER['access_token_secret']
    have_creds = True
except AttributeError:
    logger.warning('settings.TWITTER is missing. Will not be able to authenticate to Twitter.')
except KeyError as key:
    logger.warning('settings.TWITTER[%s] is missing. Will not be able to authenticate to Twitter.', key)


def tweet(message, test=False):
    logger.debug(message)

    if not have_creds:
        logger.error('Cannot tweet because there is a problem with credentials in settings.TWITTER.')
        return False

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
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
    else:
        try:
            return api.update_status(message)
        except tweepy.error.TweepError as e:
            logger.error('TweepError: %s', e)
