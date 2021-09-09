from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class SkillLevels(models.TextChoices):
    BEGINNER = 'B', _('Beginner')
    INTERMEDIATE = 'I', _('Intermediate')
    ADVANCED = 'A', _('Advanced')
    EXPERT = 'E', _('Expert')


class Skill(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        """creates and saves a new super user"""
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=225, unique=True)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)
    name = models.CharField(max_length=35)
    bio = models.CharField(max_length=256, default='', blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, through='UserSkill', blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class UserSkill(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills_data')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    level = models.CharField(
        max_length=1,
        choices=SkillLevels.choices,
        default=SkillLevels.BEGINNER)

    def __str__(self):
        return f'{self.user}_{self.skill}'

