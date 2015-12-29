# a simple module to shorten URLs, using configuration from settings

from django.conf import settings


def get_goo_gl(url):
    shortUrl = None

    try:
        data = '{longUrl:"%s", key:"%s"}' % (url, settings.GOO_GL_API_KEY)
        import urllib2

        req = urllib2.Request(settings.GOO_GL_API_URL, data)
        req.add_header('Content-type', 'application/json')
        result = urllib2.urlopen(req)
        import django.utils.simplejson as json

        shortUrl = json.loads(result.read()).get('id')
    except:
        import sys

        print('An error occurred:', sys.exc_info())

    return shortUrl


# eof
