from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# class LoggedInUser(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
#     session_key = models.CharField(max_length=32, blank=True, null=True)

#     def __str__(self):
#         return self.user.username




# permission class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class StaffPermission(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name


# staff class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff")
    permissions = models.ManyToManyField(StaffPermission)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username