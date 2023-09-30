import re
from typing import List

from oneliners.tools import commands_bash_builtins, commands_in_bsd, commands_in_gnu

# sudo bash -c 'echo ${PATH//:/\\n}' | grep -v Users | xargs -n 1 ls -1 | sort -u | awk 'BEGIN { print "commands = {" } { print sprintf("    \"%s\",", $0) } END { print "}" }'
# sudo bash -c 'echo -e ${PATH//:/\\n}' | xargs -n 1 ls -1 | sort -u | awk 'BEGIN { print "commands = {" } { print sprintf("    \"%s\",", $0) } END { print "}" }'

builtins = set()
known_commands = commands_bash_builtins.commands.union(
    commands_in_bsd.commands).union(
    commands_in_gnu.commands
)

RE_COMMAND = re.compile(r'''(?:^|[ ('])([a-zA-Z0-9][a-zA-Z0-9.+_-]*)''')
SPECIAL_COMMANDS = ['[', '[[', 'g[', '.', '((', ':']


def extract_commands_from_line(line) -> List[str]:
    matches = {
        match for match in RE_COMMAND.findall(line)
        if match in known_commands
    }

    # TODO add support for special commands
    return matches
