# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Comment(models.Model):
	comment = models.CharField(max_length=2048)
	lft = models.IntegerField()
	rgt = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
	name = models.CharField(max_length=30)