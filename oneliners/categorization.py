import abc
import dataclasses
import enum
import json
from typing import List, Dict, Any, Iterable

import openai

from oneliners.tools import rate_limiting


class CategorizationError(Exception):
    pass


class CategoryType(enum.Enum):
    FUNCTION = enum.auto()
    AUDIENCE = enum.auto()

    @staticmethod
    def parse(s: str):
        try:
            return CategoryType[s.upper()]
        except KeyError:
            raise CategorizationError(f'Unsupported category type: "{s}"')


@dataclasses.dataclass(frozen=True)
class Category:
    category_type: CategoryType
    tags: List[str]

    @staticmethod
    def parse(items: Dict[str, Any]):
        for name in 'type', 'tags':
            if name not in items:
                raise CategorizationError(f'Missing "{name}" key in dictionary: {items}')
        return Category(CategoryType.parse(items['type']), items['tags'][:])


@dataclasses.dataclass(frozen=True)
class CategorizationResult:
    raw_query: str = ''
    raw_response: str = ''
    raw_response_content: str = ''
    is_success: bool = False
    categories: List[Category] = dataclasses.field(default_factory=[])


class CategorizationComputer(abc.ABC):
    @abc.abstractmethod
    def compute_internal(self, content: str) -> CategorizationResult:
        raise NotImplementedError

    def compute(self, content: str) -> CategorizationResult:
        try:
            result = self.compute_internal(content)
        except Exception as e:
            raise CategorizationError(e)

        if not result.categories:
            raise CategorizationError("Generator returned no categories")

        return result


class OpenAiCategoriesParser:
    def parse(self, raw_response) -> List[Category]:
        return list(self._parse(raw_response))

    def _parse(self, raw_response) -> Iterable[Category]:
        try:
            d = json.loads(raw_response)
        except json.decoder.JSONDecodeError:
            raise CategorizationError(f"Could not parse as JSON: {raw_response}")

        for items in d['categories']:
            try:
                items['tags'] = [s.replace(' ', '-') for s in items['tags']]
                yield Category.parse(items)
            except CategorizationError as e:
                pass


class OpenAiCategorizationComputer(CategorizationComputer):
    def __init__(self, api_key):
        self.api_key = api_key
        self.categories_parser = OpenAiCategoriesParser()

        rate_limiter_spec = rate_limiting.RateLimiterSpec(per_minute=3, per_day=200)
        self.executor = rate_limiting.RateLimitedExecutor(rate_limiter_spec, self._compute)

    def compute_internal(self, content: str) -> CategorizationResult:
        return self.executor.execute(content)

    def _compute(self, content: str) -> CategorizationResult:
        openai.api_key = self.api_key
        query = self._format_query(content)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": query
            }],
            temperature=0,
            max_tokens=2048,
        )

        raw_response_content = response['choices'][0]['message']['content']

        return CategorizationResult(
            raw_query=query,
            raw_response=response,
            raw_response_content=raw_response_content,
            is_success=True,
            categories=self.categories_parser.parse(raw_response_content)
        )

    def _format_query(self, content: str):
        return '''
        I want to organize a collection of Bash snippets into practical and useful categories.
        For example, given this Bash one-liner content: """
        Summary: Extract the n-th field from a single line of comma separated values
        One-liner: IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"
        Explanation:
        read is a shell builtin to read fields from standard input into variables.
        The -r flag makes the command use "raw" mode, which means the input values will be stored in variables without any modifications, for example without applying escape sequences using \.
        This example specified 4 variables to store field values: first_name, _, city, and _ again. The name _ is customary for unused values. In this example we're only interested in the 1st and the 3rd fields, that's why we gave them proper names, and called the others simply _.
        When there are more fields in the input than the number of variables, all remaining fields are stored in the last variable. This is why we couldn't simply use first_name _ city without an extra _ at the end, because this way the 4th and further fields would all end up in city.
        read reads from standard input. To pass it the fixed text "John,Doe,New York,Times Square" we used the <<< operator, making this expression a so-called here-string. For more details see man bash and search for Here Strings.
        Finally, to use , as the field separator, we prefixed the call to read with IFS=,. This sets IFS only for the read command, its value in the current shell is unchanged.
        The technique is similar to cut -d, -f1,3 <<< "John,Doe,New York,Times Square", but significantly faster, because read is a builtin, and cut is an external program. Using builtins instead of commands is especially important within loops."""
        I like this categorization: """
        {
          "categories": [
            {
              "type": "Function",
              "tags": ["text processing", "data manipulation"],
              "details": "The snippet can be used to extract specific fields from comma-separated values (CSV) data. This can be useful for a variety of tasks, such as parsing log files, manipulating data in spreadsheets, and cleaning up data for analysis."
            },
            {
              "type": "Scope",
              "tags": ["general-purpose"],
              "details": "The snippet is general-purpose and can be used on any operating system that supports Bash."
            },
            {
              "type": "Complexity",
              "tags": ["intermediate"],
              "details": "The snippet is more complex than a simple Bash command, but it is still relatively easy to understand. It uses a few different features of Bash to achieve its desired result, such as the `read` command, the `IFS` variable, and the `<<<` operator."
            },
            {
              "type": "Audience",
              "tags": ["intermediate", "advanced"],
              "details": "The snippet is intended for intermediate and advanced users. It is not suitable for beginners, as it requires some knowledge of Bash and data manipulation."
            }
          ],
          "tags": ["CSV", "Bash"]
        }
        """
        Categorize this Bash one-liner, formatted as valid JSON: """%s"""
        ''' % content

