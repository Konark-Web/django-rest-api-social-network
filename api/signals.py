import datetime

from django.core.signals import request_started, request_finished
from django.dispatch import receiver

from .middleware import LoggedInUser
from network.models import CustomUser


@receiver(request_finished)
def user_last_request(sender, **kwargs):
    loggedIn = LoggedInUser()
    if loggedIn.current_user:
        user = CustomUser.objects.get(username=loggedIn.current_user)
        user.last_request = datetime.datetime.now()
        user.save()

