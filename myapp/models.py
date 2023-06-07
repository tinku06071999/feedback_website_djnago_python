from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Suggestion(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField()
    suggestion = models.TextField()

    def __str__(self):
        return self.name


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
