from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ...

class Report(models.Model):
    name = models.CharField(max_length=256)
    report_id = models.CharField(max_length=256)

