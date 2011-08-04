from django.template import Library

register = Library()

def maxlinelength(value, max_line_length=70):
    text = ''
    line = None
    for word in value.split():
	if line is None:
	    line = word
	    continue
	if len(line + ' ' + word) < max_line_length:
	    line += ' ' + word
	else:
	    text += line + '\n'
	    line = word
    text += line
    return text

register.filter(maxlinelength)

# eof
