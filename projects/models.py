from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User, Skill


class Categories(models.TextChoices):
    STARTUP = 'S', _('Startup')
    NONPROFIT = 'N', _('Nonprofit')
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
    description = models.CharField(max_length=512, default='', blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    team = models.ManyToManyField(User, through=UserProject)

    category = models.CharField(
        max_length=1,
        choices=Categories.choices,
        default=Categories.STARTUP)
    stage = models.CharField(
        max_length=1,
        choices=Stages.choices,
        default=Stages.IDEA)

    looking_for = models.CharField(max_length=512, default='', blank=True)
    skills_needed = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title
