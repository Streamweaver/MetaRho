from django.db import models
from django.contrib.auth.models import User

class CrossPostTarget(models.Model):

    user = models.ForeignKey(User)
    # crosspost target
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    post_by_default = models.BooleanField()
