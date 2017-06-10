# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Activity(models.Model):
	ip = models.CharField(max_length=50)
	browser = models.CharField(max_length=50)
	device = models.CharField(max_length=50)
	type = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)

