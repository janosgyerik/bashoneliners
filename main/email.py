from django.template import Context, loader
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend

import bashoneliners.settings as settings

BASEURL = 'http://bashoneliners.com'

FROM_EMAIL = settings.ADMINS[0][1]
BCC_EMAIL = FROM_EMAIL

def send_email(subject, message, *recipients):
    email = EmailMessage(
	    subject=subject,
	    body=message,
	    from_email=FROM_EMAIL,
	    to=recipients,
	    bcc=[ BCC_EMAIL ], 
	    )
    email.send(fail_silently=False)

def send_email_template(subject_template, subject_context, message_template, message_context, *recipients):
    message_context['baseurl'] = BASEURL
    subject = loader.get_template(subject_template).render(Context(subject_context)).strip()
    message = loader.get_template(message_template).render(Context(message_context))

    return send_email(subject, message, *recipients)

def send_oneliner_answer(question, oneliner):
    if question.user.email:
	send_email_template(
		'email/answer-sub.txt', { 'question': question, }, 
		'email/answer-msg.txt', {
		    'question': question,
		    'oneliner': oneliner,
		    },
		question.user.email
		)

def send_oneliner_alternative(oneliner, new_oneliner):
    if oneliner.user.email:
	send_email_template(
		'email/alternative-sub.txt', { 'oneliner': oneliner, }, 
		'email/alternative-msg.txt', {
		    'oneliner': oneliner,
		    'new_oneliner': new_oneliner,
		    },
		oneliner.user.email
		)

def send_oneliner_comment(oneliner, sender, comment):
    if oneliner.user.email:
	send_email_template(
		'email/comment-sub.txt', { 'oneliner': oneliner, }, 
		'email/comment-msg.txt', {
		    'oneliner': oneliner,
		    'sender': sender,
		    'comment': comment,
		    },
		oneliner.user.email
		)


class CustomFileEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
	from datetime import datetime
	import re
	if not email_messages:
	    return
	try:
	    f = open(settings.EMAIL_FILE_PATH, 'a')
	    for message in email_messages:
		context = {
			'subject': message.subject,
			'from_email': message.from_email,
			'recipients': ', '.join(message.recipients()),
			'to': ', '.join(message.to),
			'bcc': ', '.join(message.bcc),
			'body': message.body,
			'date': datetime.now(),
			}
		log = loader.get_template('email/log.txt').render(Context(context))
		log = re.sub(r'\n{3,}', '\n\n', log)
		f.write(log)
		f.flush()
	    f.close()
	    return len(email_messages)
	except:
	    return 0


# eof
