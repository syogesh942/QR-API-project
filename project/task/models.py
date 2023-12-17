from django.db import models
from django.contrib.auth.models import User

class Signup(models.Model):
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=255)
    image_type = models.CharField(max_length=50)