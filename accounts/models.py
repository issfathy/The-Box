# imports
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

# user profile model


class UserProfile(models.Model):
    # each profile is related to a user field
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(
        default="user-default.jpg", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField(
        "self", related_name='followers', blank=True, symmetrical=False)

    friend1 = models.CharField(max_length=10, null=True, blank=True)
    friend2 = models.CharField(max_length=10, null=True, blank=True)
    friend3 = models.CharField(max_length=10, null=True, blank=True)

    STATUS_OPTIONS = (
        ('away', 'Away'),
        ('online', 'Online'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    )
    status = models.CharField(
        max_length=7, choices=STATUS_OPTIONS, default='Offline')

    # string representation of user profile
    def __str__(self):
        return self.user.email


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')


class MessageModel(models.Model):
    thread = models.ForeignKey(
        'ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(
        upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


# class UserRegister(models.Model):
# 	# each profile is related to a user field
# 	# username', 'display_name', 'last_name', 'email'
# 	username = models.CharField(User, related_name='profile', on_delete=models.CASCADE, null=True)
# 	display_name = models.CharField(max_length=8)

# 	# string representation of user profile
# 	def __str__(self):
# 		return self.user.email
