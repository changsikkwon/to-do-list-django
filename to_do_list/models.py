from django import db
from django.db import models

class User(models.Model):
  account = models.CharField(max_length=32)
  password = models.CharField(max_length=32)

  class Meta:
    db_table = "user"