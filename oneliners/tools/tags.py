import re


def compute_tags_legacy(line):
    words = re.split(r'[ ;|]+', line)
    return {word for word in words if re.match(r'^[a-z_]{2,}$', word)}

