from django.db import models


class User(models.Model):
  account = models.CharField(max_length=32)
  password = models.CharField(max_length=256)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  class Meta:
    db_table = "user"