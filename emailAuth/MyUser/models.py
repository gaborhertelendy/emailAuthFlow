from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from django.utils import timezone
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import RegexValidator

from rest_framework.reverse import reverse as api_reverse


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        username = email.split('@')[0]
        user = self.model(email=email, username=username, display_name=username, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, null=True,
        help_text=_('Required. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.@+-]+$', _('Enter a valid email address.'), 'invalid')]
    )
    username = models.CharField('username', max_length=30, null=True,
        help_text=_('Optional. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')]
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    display_name = models.CharField('display_name', max_length=30, null=True,)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return str(self.email)

    def get_short_name(self):
        return str(self.email)


class Workout(models.Model):
    owner = models.ForeignKey(User, related_name='workouts', on_delete=models.CASCADE)
    # delete the workout if user is deleted, note that default generated workout_set
    # is overwritten with 'workout' (related_name) property
    efficiency = models.FloatField(default=0)
    exercises = models.FloatField(default=0)  # This should be JSON

    date = models.DateTimeField('dateTime of the workout', auto_now_add=True)  # Should be just date

    def __str__(self):
        return str(self.date)


# Profile can be an extension on User by OneToOne linking them together
# In our implementation we decided to simply include the profile related fields in the user
# If you want to use profile instead, uncomment this part, remove the desired fields from User
# and move them to profile.
#   NOTE: This may cause extra DB queries
#       (use: users = User.objects.all().select_related('profile') to prefetch when needed)

# class Profile(models.Model):
#     owner = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     display_name = models.CharField('display_name', max_length=30, null=True,
#         help_text=_('Optional. 30 characters or fewer.')
#     )
#
#     def __str__(self):
#         return str(self.display_name)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(owner=instance, display_name=instance.username)
#
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
