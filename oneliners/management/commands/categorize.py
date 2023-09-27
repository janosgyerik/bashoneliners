from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from oneliners import categorization, models


class Command(BaseCommand):
    help = 'Update category tags of one-liners'

    def add_arguments(self, parser):
        parser.add_argument("pk", nargs="*", type=int)
        parser.add_argument("--all", action='store_true')

    def handle(self, *args, **options):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise CommandError(f"settings.OPENAI_API_KEY is blank. Try with --settings bashoneliners.local_settings")

        categorizer = categorization.OpenAiCategorizationComputer(api_key)
        adapter = models.CategorizationAdapter()

        oneliners = models.OneLiner.objects.filter(onelinercategory__isnull=True)
        if not options['all']:
            pklist = options['pk']
            oneliners = oneliners.filter(pk__in=pklist)

        for oneliner in oneliners:
            content = (
                f"Summary: '''{oneliner.summary}'''\n"
                f"One-liner: '''{oneliner.line}'''\n"
                f"Explanation: '''{oneliner.explanation}'''\n"
                f"Limitations: '''{oneliner.limitations}'''\n"
            )
            self.stdout.writelines([
                "Computing categories for one-liner:",
                content,
            ])

            response = categorizer.compute(content)
            self.stdout.writelines([str(response.raw_response)])
            self.stdout.writelines([str(response.raw_response_content)])
            self.stdout.writelines([str(s) for s in response.categories])
            self.stdout.writelines([""])

            categories = []
            for category in response.categories:
                categories.extend(adapter.convert_category(category))

            oneliner.set_categories(categories)
