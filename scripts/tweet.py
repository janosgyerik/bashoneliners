#!/usr/bin/env python
# 
# To access twitter with OAuth, you need to first obtain:
#	consumer key, consumer secret, access token, access token secret
#
# 1. Login to Twitter
# 2. Go to https://dev.twitter.com/apps/new and fill the form
#	- Application Type should be Client
#	- Default Access Type must be Read and Write
# 3. Consumer key and secret are here: https://dev.twitter.com/apps
# 4. Access token and secret are in the My Access Token menu
#

''' hack to setup django environment START '''
import sys
sys.path.append('..')
import settings
from django.core.management import setup_environ
setup_environ(settings)
''' hack to setup django environment END '''

from django.db.models import Max
from datetime import timedelta, datetime
from bashoneliners.main.models import OneLiner
from bashoneliners.main.views import tweet

import optparse
import os

try:
    consumer_key = settings.TWITTER.get('consumer_key')
    consumer_secret = settings.TWITTER.get('consumer_secret')
    access_token = settings.TWITTER.get('access_token')
    access_token_secret = settings.TWITTER.get('access_token_secret')
except:
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.set_usage('%prog [options]')
    parser.set_description('Tweet specified one-liners by @bashoneliners')

    parser.add_option('--pk', '--id', help='The pk/id of the OneLiner to tweet', type=int, action='append')
    parser.add_option('--recent', help='List recent OneLiners, do not tweet', action='store_true', default=False)
    parser.add_option('--send', help='Send tweets', action='store_true', default=False)

    (options, args) = parser.parse_args()

    if not (consumer_key and consumer_secret and access_token and access_token_secret):
	if not consumer_key:
	    print 'Error: Consumer Key is required!'
	if not consumer_secret:
	    print 'Error: Consumer Secret is required!'
	if not access_token:
	    print 'Error: Access Token is required!'
	if not access_token_secret:
	    print 'Error: Access Token Secret is required!'
	parser.print_help()
	parser.exit()
    
    if options.recent:
	for oneliner in OneLiner.recent()[:10]:
	    print oneliner.pk,
	    print oneliner.summary
	    print oneliner.line
	    print
	parser.exit()

    if options.pk:
	for pk in options.pk:
	    oneliner = OneLiner.objects.get(pk=pk)

	    if options.send:
		print tweet(oneliner, force=True)
	    else:
		print tweet(oneliner, force=True, test=True)

# eof
