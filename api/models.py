from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True, related_query_name="custom_user")
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        related_query_name="custom_user"
    )

    def __str__(self):
        return self.username
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')

    def __str__(self):
        return self.title
