from django.test import TestCase

from oneliners.tools import commands as lib


class KnownCommandTests(TestCase):
    def test_all_known_commands_match_commands_pattern(self):
        failed_commands = []
        for command in lib.known_commands:
            if command not in lib.SPECIAL_COMMANDS and not lib.RE_COMMAND.match(command):
                failed_commands.append(command)

        self.assertEqual(
            0,
            len(failed_commands),
            msg=f"{len(failed_commands)} command(s) do not match known patterns: {failed_commands[:3]}",
        )

    def test_extract_commands_from_line_finds_known_commands(self):
        for command in lib.known_commands:
            if command in lib.SPECIAL_COMMANDS:
                continue
            self.assertEqual({command}, lib.extract_commands_from_line(command))


class ExtractCommandsTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_extractor = lib.extract_commands_from_line

    def test_finds_correct_commands_from_pipeline(self):
        line = r"cut -d ':' -f 1,3 /etc/passwd | sort -t ':' -k2n - | tr ':' '\t'"
        self.assertEqual({"cut", "sort", "tr"}, self.command_extractor(line))

    def test_finds_commands_embedded_in_subcommands(self):
        line = r"watch -n 1 'ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head'"
        self.assertEqual({"watch", "ps", "head"}, self.command_extractor(line))

    def test_finds_correct_commands_from_semicolon_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel*; cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_correct_commands_from_doubleamperstand_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* && cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_correct_commands_from_doublepipe_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* || cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_commands_from_pipeline(self):
        line = r"cut -d ':' -f 1,3 /etc/passwd | sort -t ':' -k2n - | tr ':' '\t'"
        self.assertEqual({"cut", "sort", "tr"}, self.command_extractor(line))

    def test_finds_commands_from_semicolon_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel*; cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_commands_from_doubleamperstand_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* && cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_commands_from_doublepipe_separated(self):
        line = r'''echo /etc/*_ver* /etc/*-rel* || cat /etc/*_ver* /etc/*-rel*'''
        self.assertEqual({"echo", "cat"}, self.command_extractor(line))

    def test_finds_command_after_single_variable_assignment_prefix(self):
        line = r'''IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_after_single_variable_assignment_with_singlequoted_value_prefix(self):
        line = r'''IFS=' ' read -r first_name _ city _ <<< "John Doe New York Times-Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_after_single_variable_assignment_with_doublequoted_value_prefix(self):
        line = r'''IFS=" " read -r first_name _ city _ <<< "John Doe New York Times-Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_after_repeated_single_variable_assignment_prefix(self):
        line = r'''k=v IFS=, read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_after_single_variable_assignment_command(self):
        line = r'''IFS=,; read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_after_repeated_variable_assignment_prefixes_of_intermixed_styles(self):
        line = r'''a=b IFS=',' c=d; x=y read -r first_name _ city _ <<< "John,Doe,New York,Times Square"'''
        self.assertEqual({"read"}, self.command_extractor(line))

    def test_finds_command_from_group(self):
        variations = (
            '{ echo; }',
            '{ echo; }; echo',
            '{ echo foo; }',
            '{ echo "foo"; }',
            '{ k=v echo; }',
            '{ k=v a=b echo; }',
        )
        for line in variations:
            self.assertEqual({"echo"}, self.command_extractor(line), msg=f"for line: {line}")

    def test_finds_command_from_subshell_group(self):
        variations = (
            '(echo)',
            '(echo); echo',
            '(echo); k=v echo',
            '(echo foo)',
            '(echo "foo")',
            '(k=v echo)',
            '(k=v a=b echo)',
        )
        for line in variations:
            self.assertEqual({"echo"}, self.command_extractor(line), msg=f"for line: {line}")

    # TODO add support for [ and [[
    def _test_finds_square_brackets_from_test_command_variations(self):
        variations = (
            '[ a = b ]; echo $?',
            '[ a = b ] && echo $?',
            '[ a = b ] || echo $?',
        )
        for line in variations:
            self.assertEqual({"[", "echo"}, self.command_extractor(line), msg=f"for line: {line}")

        variations = (
            '[[ a = b ]]; echo $?',
            '[[ a = b ]] && echo $?',
            '[[ a = b ]] || echo $?',
        )
        for line in variations:
            self.assertEqual({"[[", "echo"}, self.command_extractor(line), msg=f"for line: {line}")
