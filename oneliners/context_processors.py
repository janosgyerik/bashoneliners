from django.conf import settings

def google_analytics(request):
    import logging
    logger = logging.getLogger(__name__)
    logger.debug('ga = %s', settings.GOOGLE_ANALYTICS_ID)
    return {
            'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
            }
