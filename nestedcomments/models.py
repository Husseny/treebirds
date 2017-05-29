# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
import sys
from collections import namedtuple

# Create your models here.

class Comment(models.Model):
	comment = models.CharField(max_length=2048)
	lft = models.IntegerField()
	rgt = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	@classmethod
	def add_comment(cls, comment):
		with connection.cursor() as cursor:
			cursor.execute('SELECT MAX(rgt) AS max FROM comment')
			comments = namedtuplefetchall(cursor)
			if None in comments:
				max_right = 0
			else:
				max_right = comments[0].max
			new_left = max_right + 1
			new_right = new_left + 1
			cursor.execute('INSERT INTO comment (comment, rgt, lft, created_at) VALUES (%s, %s, %s, NOW())',[comment, new_right, new_left])
			return True

class User(models.Model):
	name = models.CharField(max_length=30)

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]