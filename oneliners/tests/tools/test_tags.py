from django.test import TestCase

from oneliners.tools import tags as tag_tools


class LegacyTagsTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_extractor = tag_tools.compute_tags_legacy

    def test_finds_correct_commands_from_pipeline(self):
        line = r"cut -d ':' -f 1,3 /etc/passwd | sort -t ':' -k2n - | tr ':' '\t'"
        self.assertEqual({"cut", "sort", "tr"}, self.tag_extractor(line))

    def test_incorrectly_finds_name_params_of_read(self):
        line = r'''IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        # This is wrong!
        self.assertEqual({"read", "first_name", "city"}, self.tag_extractor(line))

        # Ideally this should be:
        # self.assertEqual({"read"}, self.tag_extractor(line))

    def test_does_not_find_commands_embedded_in_subcommands(self):
        line = r"watch -n 1 'ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head'"
        # This is reasonable: picking up "ps" and "head" would require
        # knowing the implementation detail of the "watch" command,
        # which is not a Bash builtin.
        self.assertEqual({"watch"}, self.tag_extractor(line))

        # Ideally this should be:
        # self.assertEqual({"watch", "ps", "head"}, self.tag_extractor(line))

    def test_finds_correct_commands_semicolon_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel*; cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.tag_extractor(line))

    def test_finds_correct_commands_doubleamperstand_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* && cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.tag_extractor(line))

    def test_finds_correct_commands_doublepipe_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* || cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.tag_extractor(line))


class TagsAsFirstCommandTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_extractor = tag_tools.compute_tags_as_first_command

    def test_finds_first_command_from_pipeline(self):
        line = r"cut -d ':' -f 1,3 /etc/passwd | sort -t ':' -k2n - | tr ':' '\t'"
        self.assertEqual({"cut"}, self.tag_extractor(line))

    def test_finds_first_command_from_semicolon_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel*; cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo"}, self.tag_extractor(line))

    def test_finds_first_command_from_doubleamperstand_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* && cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo"}, self.tag_extractor(line))

    def test_finds_first_command_from_doublepipe_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* || cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo"}, self.tag_extractor(line))

    def test_finds_first_command_after_single_variable_assignment_prefix(self):
        line = r'''IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_first_command_after_single_variable_assignment_with_singlequoted_value_prefix(self):
        line = r'''IFS=' ' read -r first_name _ city _ <<< "John Doe New York Times-Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_first_command_after_single_variable_assignment_with_doublequoted_value_prefix(self):
        line = r'''IFS=" " read -r first_name _ city _ <<< "John Doe New York Times-Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_first_command_after_repeated_single_variable_assignment_prefix(self):
        line = r'''k=v IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_first_command_after_single_variable_assignment_command(self):
        line = r'''IFS=,; read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_first_command_after_repeated_variable_assignment_prefixes_of_intermixed_styles(self):
        line = r'''a=b IFS=',' c=d; x=y read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.tag_extractor(line))

    def test_finds_empty_set_for_unsopported_patterns(self):
        # Make sure we don't extract commands incorrectly.
        bad_examples = (
            "echo;echo",
            "k=v;echo",
        )

        # We should add support for all these patterns, they should return { "echo" }.
        unsupported_examples = (
            'fun() { echo; }',
            'fun() { local a; echo; }',
            'fun() { local a b; echo; }',
            'fun() { local a=b; echo; }',
            'fun() { local a=b b=c; echo; }',
            '{ echo path; }',
            '(echo path)',
            '[ a = b ]; echo $?',
            '[ a = b ] && echo $?',
            '[ a = b ] || echo $?',
            '[[ a = b ]]; echo $?',
            '[[ a = b ]] && echo $?',
            '[[ a = b ]] || echo $?',
            '&> /dev/null echo',
        )

        for line in bad_examples + unsupported_examples:
            self.assertEqual(set(), self.tag_extractor(line))

