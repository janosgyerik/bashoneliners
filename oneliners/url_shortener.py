# a simple module to shorten URLs, using configuration from settings

import requests

from logging import getLogger

logger = getLogger(__name__)


def shorten(url):
    try:
        result = requests.get('http://tinyurl.com/api-create.php?url={}'.format(url))
        if result.status_code != 200:
            logger.error('Unexpected response from url shortener: status={}; text={}'.format(
                result.status_code, result.text))
            return

        return result.text
    except Exception as e:
        logger.error('Could not create short url for {}: {}'.format(url, e))
