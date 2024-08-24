from django.contrib import auth
from django.db import models
from django.utils import timezone


class User(auth.models.User, auth.models.PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)




# class Group(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

# class GroupMember(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
