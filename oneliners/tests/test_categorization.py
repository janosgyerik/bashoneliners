from django.test import TestCase

from oneliners import categorization as lib


class CategorizationTests(TestCase):

    def test_category_type_parse_supports_lowercase_function(self):
        self.assertEqual(lib.CategoryType.FUNCTION, lib.CategoryType.parse("function"))

    def test_category_type_parse_supports_titlecase_function(self):
        self.assertEqual(lib.CategoryType.FUNCTION, lib.CategoryType.parse("Function"))

    def test_category_type_parse_supports_audience(self):
        self.assertEqual(lib.CategoryType.AUDIENCE, lib.CategoryType.parse("audience"))

    def test_category_type_parse_raises_for_nonexistent(self):
        with self.assertRaises(lib.CategorizationError) as context:
            lib.CategoryType.parse('nonexistent')

        self.assertRegexpMatches(str(context.exception), r'Unsupported category type')

    def test_category_parse_supports_well_formed_content(self):
        items = {
            "type": "Function",
            "tags": ["system-monitoring", "memory-usage"],
            "details": "Dummy details."
        }
        category = lib.Category.parse(items)
        self.assertEqual(lib.CategoryType.FUNCTION, category.category_type)
        self.assertEqual(["system-monitoring", "memory-usage"], category.tags)

    def test_category_parse_raises_when_type_missing(self):
        items = {
            "tags": ["system-monitoring", "memory-usage"],
            "details": "Dummy details."
        }
        with self.assertRaises(lib.CategorizationError) as context:
            lib.Category.parse(items)

        self.assertRegexpMatches(str(context.exception), r'Missing "type" key')

    def test_category_parse_raises_when_tags_missing(self):
        items = {
            "type": "Function",
            "details": "Dummy details."
        }
        with self.assertRaises(lib.CategorizationError) as context:
            lib.Category.parse(items)

        self.assertRegexpMatches(str(context.exception), r'Missing "tags" key')


class OpenAiCategoriesParserTests(TestCase):
    def test_parse_sample_response(self):
        text = '''{
  "categories": [
    {
      "type": "Function",
      "tags": ["system monitoring", "memory usage"],
      "details": "The snippet can be used to retrieve the Proportional Set Size (PSS) memory usage of a specific Linux process. This can be useful for monitoring the memory usage of a process and identifying potential memory leaks or inefficiencies."
    },
    {
      "type": "Scope",
      "tags": ["Linux"],
      "details": "The snippet is specific to Linux and relies on the /proc filesystem to access process memory accounting details."
    },
    {
      "type": "Complexity",
      "tags": ["intermediate"],
      "details": "The snippet involves multiple commands and uses various text processing tools such as grep, tr, and cut. It requires some understanding of Linux process memory accounting and command-line tools."
    },
    {
      "type": "Audience",
      "tags": ["intermediate", "advanced"],
      "details": "The snippet is intended for intermediate and advanced users who are familiar with Linux and command-line tools. It may not be suitable for beginners."
    }
  ],
  "tags": ["Linux", "memory usage", "process monitoring"]
}'''
        categories = lib.OpenAiCategoriesParser().parse(text)
        c1 = lib.Category(lib.CategoryType.FUNCTION, ["system-monitoring", "memory-usage"])
        c2 = lib.Category(lib.CategoryType.AUDIENCE, ["intermediate", "advanced"])
        self.assertEqual([c1, c2], categories)
