from social.celery import app
from .service import send_email
from .models import Subscribers, Post

from django.utils.html import strip_tags
from django.contrib.sites.models import Site


@app.task
def send_email_to_user(email):
    send_email('Subscribed successful', 'Congratulations! You subscribed on new posts.', email)


@app.task
def send_posts():
    domain = Site.objects.get_current().domain
    for subscriber in Subscribers.objects.filter(status=1):
        text_html = 'Our posts:\n<ul>'
        for post in Post.objects.all():
            text_html += f'<li><a href="http://{domain}/post/{post.id}">{post.title}</a></li>\n'
        text_html += '</ul>'

        plain_message = strip_tags(text_html)
        send_email('[NEW] We have new posts', plain_message, subscriber.email, text_html)
