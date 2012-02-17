from django.template import Context, loader
from django.core.mail import EmailMessage

import bashoneliners.settings as settings

BASEURL = 'http://bashoneliners.com'

FROM_EMAIL = settings.ADMINS[0][1]
BCC_EMAIL = FROM_EMAIL

def send_email(subject, message, *recipients):
    email = EmailMessage(
	    subject = subject,
	    body = message,
	    from_email = FROM_EMAIL,
	    to = recipients,
	    bcc = [ BCC_EMAIL ], 
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


# eof
