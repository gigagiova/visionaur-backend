from django.db import models
from django.utils.translation import gettext_lazy as _

from social.models import Update
from users.models import User, Skill


class Categories(models.TextChoices):
    STARTUP = 'S', _('Startup')
    NONPROFIT = 'N', _('Nonprofit')
    SIDEPROJECT = 'P', _('Side Project')
    RESEARCH = 'R', _('Research')


class Stages(models.TextChoices):
    IDEA = 'I', _('Idea stage')
    PROTOTYPE = 'P', _('Prototype')
    COMPLETED = 'C', _('Completed')


class Roles(models.TextChoices):
    FOUNDER = 'F', _('Founder')
    ADMIN = 'A', _('Admin')
    MEMBER = 'M', _('Member')


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='members')

    role = models.CharField(
        max_length=1,
        choices=Roles.choices,
        default=Roles.MEMBER)


class Project(models.Model):

    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='', blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    team = models.ManyToManyField(User, through=UserProject)
    repository = models.CharField(max_length=512, null=True, blank=True)

    # not really useful for now
    category = models.CharField(
        max_length=1,
        choices=Categories.choices,
        default=Categories.SIDEPROJECT)
    stage = models.CharField(
        max_length=1,
        choices=Stages.choices,
        default=Stages.IDEA)

    looking_for = models.CharField(max_length=512, null=True, blank=True)
    skills_needed = models.ManyToManyField(Skill, blank=True)
    updates = models.ManyToManyField(Update, blank=True)

    def __str__(self):
        return self.title

    def user_role(self, user):
        # return the role of this user, None if it is not part of the team
        return self.members.filter(user=user).first().role

    class Meta:
        ordering = ('-created',)
