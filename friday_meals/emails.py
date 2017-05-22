from django.core.mail import send_mail
from django.template.loader import render_to_string
from friday_meals.utils import CURRENT_WEEK
import threading

#all instances to "RECIPIENTS" should be replaced with real email addresses

class EmailThread(threading.Thread):
    def __init__(self, subject, html_message, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list # for testing purposes
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, 'body text?', 'from@example.com', self.recipient_list, html_message=self.html_message)


def notify_user_deleted_meal(user):

    html = render_to_string(
        'friday_meals/email-notify-user.html',
        {'user':user})

    subject = 'Deleted meal from order!'
    body = 'This should be replaced with HTML message'
    from_ = 'from@example.com'
    to_ = [user.email]
    html_message = html

    EmailThread(subject, html_message, to_).start()


def notify_staff_to_order(lista, suma):
    html = render_to_string(
        'friday_meals/email-notify-staff.html', {
        'lista': lista,
        'suma': suma
    })

    subject = 'Order for week # %s is ready!' % CURRENT_WEEK
    body = 'This should be replaced with HTML message'
    from_ = 'from@example.com'
    to_ = ['donfrozex@gmail.com']
    html_message = html

    EmailThread(subject, html_message, to_).start()


def send_user_token(token, user):
    html = render_to_string(
        'friday_meals/email-activation-token.html', {
            'token': token,
            'user': user
        })

    subject = 'Activate your account!'
    body = 'This should be replaced with HTML message'
    from_ = 'from@example.com'
    to_ = [user.email]
    html_message = html

    EmailThread(subject, html_message, to_).start()
