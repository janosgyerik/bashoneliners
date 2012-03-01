# a simple module to tweet a message, using configuration from settings

import settings

def tweet(message, test=False, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    try:
	import tweepy # 3rd party lib, install with: easy_install tweepy
	if consumer_key is None:
	    consumer_key = settings.TWITTER.get('consumer_key')
	if consumer_secret is None:
	    consumer_secret = settings.TWITTER.get('consumer_secret')
	if access_token is None:
	    access_token = settings.TWITTER.get('access_token')
	if access_token_secret is None:
	    access_token_secret = settings.TWITTER.get('access_token_secret')

	# set up credentials to use Twitter api.
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	if len(message) > 139:
	    message = message[:135] + ' ...'
	
	if test:
	    print message
	    print
	    return True
	else:
	    return api.update_status(message)
    except:
	import sys
	print 'An error occurred:', sys.exc_info()


# eof
