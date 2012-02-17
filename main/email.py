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


# eof
