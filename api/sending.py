from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

class CodeSendingFailed(Exception):
    pass


def send_verification_code(user, code):
    sender = getattr(settings, 'JWT2FA_AUTH.CODE_SENDER', None)
    return sender(user, code)


def send_verification_code_via_email(user, code):
    user_email_address = getattr(user, 'email', None)

    if not user_email_address:
        raise CodeSendingFailed(_("No e-mail address known"))

    subject_template = _(
         getattr(settings, 'JWT2FA_AUTH.EMAIL_SENDER_SUBJECT_OVERRIDE', None) or
        _("{code}: Your verification code"))
    body_template = (
        getattr(settings, 'JWT2FA_AUTH.EMAIL_SENDER_BODY_OVERRIDE', None)  or
        _("{code} is the verification code needed for the login."))

    # messages_sent_v2 = send_mail(
    #      subject_template.format(code=code),
    #      body_template.format(code=code), 
    #      'regiojosh1@gmail.com',
    #      [user_email_address],
    #      fail_silently=False)

    messages_sent = send_mail(
        subject=subject_template.format(code=code),
        message=body_template.format(code=code),
        from_email = getattr(settings, 'DEFAULT_FROM', None),
        recipient_list=[user_email_address],
        fail_silently=True)
    if not messages_sent:
        raise CodeSendingFailed(_("Unable to send e-mails"))