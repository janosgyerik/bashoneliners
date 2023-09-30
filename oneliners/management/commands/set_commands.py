import logging
import sys

from django.core.management.base import BaseCommand

from oneliners import models

# Is there a better way to activate logging to stdout in Django management commands?
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Set command tags of one-liners'

    def add_arguments(self, parser):
        parser.add_argument("pk", nargs="*", type=int)
        parser.add_argument("--all", action='store_true')

    def handle(self, *args, **options):
        oneliners = models.OneLiner.objects.filter(onelinercommand__isnull=True)
        if not options['all']:
            pklist = options['pk']
            oneliners = oneliners.filter(pk__in=pklist)

        for oneliner in oneliners:
            logger.info(f'Setting commands for oneliner: {oneliner.line}')
            oneliner.update_commands()

            logger.info(f'Detected ommands for oneliner: {oneliner.get_commands()}')
