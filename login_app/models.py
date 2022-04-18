from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Failed_count(models.Model):
    count = models.IntegerField()
    updated_timestamp = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
