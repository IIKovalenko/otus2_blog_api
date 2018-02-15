from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=512)
    body = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.user.username)
