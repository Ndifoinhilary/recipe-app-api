import os
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import ManyToManyField


# Create your models here.

def recipe_image_path(instance, filename):
    """
    Generate file path for new recipe image
    :param instance:
    :param filename:
    :return:
    """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'recipes', filename)



class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers.
    """
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class Recipe(models.Model):
    """
    Custom recipe model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to=recipe_image_path, null=True, blank=True)
    tag = ManyToManyField('Tag', related_name='recipes')
    ingredients = ManyToManyField('Ingredient', related_name='recipes')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Custom tags model
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Custom ingredient model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name
