from django.core import mail
from templated_mail.mail import BaseEmailMessage


def test_mail_send_successful(mailoutbox):
    """
    Test Emails are send out
    """
    mail.send_mail('subject', 'body', 'from@example.com', ['to@example.com'])
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert m.subject == 'subject'
    assert m.body == 'body'
    assert m.from_email == 'from@example.com'
    assert list(m.to) == ['to@example.com']


def test_mail_send_custom_template_successful(mailoutbox):
    """
    Test Djoser Custom Templates are Used
    """
    BaseEmailMessage(
        template_name='auth/username_changed_confirmation.html').send(to=['foo@bar.tld'])
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert list(m.to) == ['foo@bar.tld']
