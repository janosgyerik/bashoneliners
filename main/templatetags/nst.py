from django.template import Library

register = Library()

import re

def nst(value):
    value = re.sub(r'<.*?>', '', value)
    value = re.sub(r'\n', '<br/>', value)
    value = re.sub(r'{{(?P<cmd>.*?)}}', '<code>\g<cmd></code>', value)
    return value

register.filter(nst)

# eof
