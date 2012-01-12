from django.template import Library

register = Library()

import re

def nst(value):
    value = re.sub(r'<.*?>', '', value)
    value = re.sub('&', '&amp;', value)
    value = re.sub('<', '&lt;', value)
    value = re.sub('>', '&gt;', value)
    value = re.sub(r'\n', '<br/>', value)
    value = re.sub(r'{{(?P<cmd>.*?)}}', '<code>\g<cmd></code>', value)
    return value

register.filter(nst)

# eof
