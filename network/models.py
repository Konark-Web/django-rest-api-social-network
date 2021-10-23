from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    last_request = models.DateTimeField(default=timezone.now)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    @property
    def date_modified(self):
        return f'{self.created_date:%d %b %Y}'


class PostLikes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
