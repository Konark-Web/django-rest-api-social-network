from django.core.mail import send_mail


def send_email(subject, text, email, html=None):
    send_mail(subject,
              text,
              'konark666@gmail.com',
              [email],
              fail_silently=False,
              html_message=html)
