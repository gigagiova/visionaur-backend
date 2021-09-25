from django.db import models

from projects.models import Project
from social.models import Comment, Update
from users.models import User


class ChallengeProject(models.Model):
    challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE, related_name='subscribed_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='challenges')
    winner = models.BooleanField(default=False)


class Challenge(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='', blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.CharField(null=True, blank=True, max_length=64)

    looking_for_team = models.ManyToManyField(User, related_name='looking_to_join')
    projects = models.ManyToManyField(Project, through=ChallengeProject)
    organizers = models.ManyToManyField(User, related_name='challenges_organized')
    comments = models.ManyToManyField(Comment, related_name='root')
    updates = models.ManyToManyField(Update, related_name='challenge')

    class Meta:
        ordering = ('-created',)
