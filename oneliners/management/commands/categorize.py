from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from oneliners import categorization, models


class Command(BaseCommand):
    help = 'View and manipulate the tags of one-liners'

    def add_arguments(self, parser):
        parser.add_argument("pk", nargs="*", type=int)

    def handle(self, *args, **options):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise CommandError(f"settings.OPENAI_API_KEY is blank. Try with --settings bashoneliners.local_settings")

        categorizer = categorization.OpenAiCategorizationComputer(api_key)

        pklist = options['pk']
        for pk in pklist:
            oneliner = models.OneLiner.get(pk)
            content = (
                f"Summary: {oneliner.summary}\n"
                f"One-liner: {oneliner.line}\n"
                f"Explanation: {oneliner.explanation}\n"
                f"Limitations: {oneliner.limitations}\n"
            )

            response = categorizer.compute(content)
            print(response.raw_response)
            print(response.raw_response_content)
            for category in response.categories:
                print(category)