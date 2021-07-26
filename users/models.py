from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """creates and saves a new super user"""
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=225, unique=True)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    bio = models.CharField(max_length=256, default='')
    profile_pic = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
