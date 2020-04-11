from django.contrib.auth.models import User
from django.db import models


class UserOffice365ID(models.Model):
    user = models.ForeignKey(User)
    office365_id = models.TextField()
