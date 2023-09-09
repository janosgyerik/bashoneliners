import re


def compute_tags_legacy(line):
    words = re.split(r'[ ;|]+', line)
    return {word for word in words if re.match(r'^[a-z_]{2,}$', word)}


def compute_tags_as_first_command(line):
    # Supported patterns:
    # cat ...
    # v=... cat ...
    # v=... k=... cat ...
    # v=...; cat ...
    # v=... k=...; x= cat ...
    # { cat ...; }
    # (cat ...)
    # [ ... ]
    # [[ ... ]]

    # Unsupported patterns that normally should return { "sudo", "cat" }
    # sudo cat ...
    # sudo -s cat ...

    # Unsupported patterns that normally should return { "cat" }
    # fun() { cat ...; }
    # fun() { local v; cat ...; }
    # &> /dev/null cat ...

    # Strip variable assignment prefixes or commands, repeatedly.
    while True:
        orig = line
        line = re.sub(r"^[a-zA-Z][a-zA-Z0-9_]*='[^']*';? *", "", line)
        line = re.sub(r'^[a-zA-Z][a-zA-Z0-9_]*="[^"]*";? *', "", line)
        line = re.sub(r"^[a-zA-Z][a-zA-Z0-9_]*=[^ ]*;? *", "", line)
        line = re.sub(r"^{ ([^{}]+); }.*", r"\1", line)
        line = re.sub(r"^\(([^()]+)\).*", r"\1", line)
        if line == orig:
            break

    match = re.match(r'^(?P<command>[a-z][a-z0-9]+)( |$)', line)
    if match:
        return {match.group('command')}

    match = re.match(r'^(?P<command>(\[|\[\[)) ', line)
    if match:
        return {match.group('command')}

    return set()
