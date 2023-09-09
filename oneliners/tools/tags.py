import re


def compute_tags_legacy(line):
    words = re.split(r'[ ;|]+', line)
    return {word for word in words if re.match(r'^[a-z_]{2,}$', word)}


def compute_tags_as_first_command(line):
    # Supported patterns:
    # cat ...
    # v=... cat ...
    # v=...; cat ...

    # Unsupported patterns
    # { cat ...; }
    # (cat ...)
    # sudo cat ...
    # sudo -s cat ...
    # [ ... ]
    # [[ ... ]]
    # fun() { cat ...; }
    # fun() { local v; cat ...; }
    # &> /dev/null cat ...

    # Strip variable assignment prefixes or commands.
    line = re.sub(r"^[a-zA-Z][a-zA-Z0-9_]+='[^']*';? *", "", line)
    line = re.sub(r'^[a-zA-Z][a-zA-Z0-9_]+="[^"]*";? *', "", line)
    line = re.sub(r"^[a-zA-Z][a-zA-Z0-9_]+=[^ ]*;? *", "", line)

    match = re.match(r'^(?P<command_name>[a-z][a-z0-9]+)', line)
    if match:
        return {match.group('command_name')}
    return set()
