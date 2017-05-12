from django.core.mail import send_mail
from django.template.loader import render_to_string
from friday_meals.utils import CURRENT_WEEK

def notify_user_deleted_meal(user):

    html = render_to_string(
        'friday_meals/email-notify-user.html',
        {'user':user})

    send_mail(
        'Deleted meal from order!',
        'body text',
        'from@example.com',
        [user.email],
        fail_silently=False,
        html_message=html,
    )


def notify_staff_to_order(lista, suma):

    html = render_to_string(
        'friday_meals/email-notify-staff.html', {
        'lista': lista,
        'suma': suma
    })

    send_mail(
        'Order for week # %s is ready!' % CURRENT_WEEK,
        'body text',
        'from@example.com',
        ['donfrozex@gmail.com'],
        fail_silently=False,
        html_message=html,
    )


def send_user_token(token, user):
    html = render_to_string(
        'friday_meals/email-activation-token.html', {
            'token': token,
            'user': user
        })

    send_mail(
        'Activate your account!',
        'body text',
        'from@example.com',
        ['donfrozex@gmail.com'],
        fail_silently=False,
        html_message=html,
    )