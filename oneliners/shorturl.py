# a simple module to shorten URLs, using configuration from settings

import requests
import json

from django.conf import settings


def get_goo_gl(url):
    if not settings.GOO_GL_API_KEY:
        return None

    try:
        data = {'longUrl': url}
        request_url = '{}?key={}'.format(settings.GOO_GL_API_URL, settings.GOO_GL_API_KEY)
        headers = {'Content-Type': 'application/json'}

        result = requests.post(request_url, data=json.dumps(data), headers=headers)
        return json.loads(result.content.decode()).get('id')
    except:
        import sys

        print('An error occurred:', sys.exc_info())

    return None
