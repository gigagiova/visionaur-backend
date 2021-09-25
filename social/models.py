from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User


class Comment(models.Model):
    text = models.CharField(max_length=1024)
    by_user = models.ForeignKey(User, related_name='comment_activity', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    children = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f'by {self.by_user} at {self.created}'


class Update(models.Model):
    text = models.CharField(max_length=2048)
    by_user = models.ForeignKey(User, related_name='update_activity', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return f'update by {self.by_user} at {self.created}'

    class Meta:
        ordering = ('-created',)


class Notification(models.Model):
    class Verbs(models.TextChoices):
        INVITE_TO_PROJECT = 'IP'

    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(
        max_length=2,
        choices=Verbs.choices,
        default=Verbs.INVITE_TO_PROJECT)
    object_slug = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
