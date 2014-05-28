from ummeli.base.utils import render_to_pdf
from django.core.mail import EmailMessage

from celery.task import task


@task
def schedule_cv_email(cv,  email_address,  email_text, from_address):
    email = EmailMessage('CV for %s' % cv.fullname(), email_text,
                         from_address,
                         [email_address], ['ummeli@praekeltfoundation.org'])
    pdf = render_to_pdf('pdf_template.html', {'model': cv})
    email.attach(
        'curriculum_vitae_for_%s_%s.pdf' % (cv.first_name, cv.surname),
        pdf,  'application/pdf')
    email.send(fail_silently=False)
