# a simple module to shorten URLs, using configuration from settings

import logging
import requests

logger = logging.getLogger(__name__)


def shorten(url):
    try:
        logger.info(f"shorten={url}")
        result = requests.get('http://tinyurl.com/api-create.php?url={}'.format(url))
        if result.status_code != 200:
            logger.error('Unexpected response from url shortener: status={}; text={}'.format(
                result.status_code, result.text))
            return

        shortened = result.text
        logger.info(f"shortened={shortened}")
        return shortened

    except Exception as e:
        logger.error('Could not create short url for {}: {}'.format(url, e))
