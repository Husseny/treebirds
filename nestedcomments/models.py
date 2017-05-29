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
			max_right = comments[0].max
			if max_right == None:
				max_right = 0
			new_left = max_right + 1
			new_right = new_left + 1
			cursor.execute('INSERT INTO comment (comment, rgt, lft, created_at) VALUES (%s, %s, %s, NOW())',[comment, new_right, new_left])
			return True

	@classmethod
	def add_nested_comment(cls, parent_comment_id, comment):
		with connection.cursor() as cursor:
			cursor.execute('SELECT rgt as parent_right FROM comment WHERE id = %s',[parent_comment_id])
			parent_comment = namedtuplefetchall(cursor)
			parent_right = parent_comment[0].parent_right
			cursor.execute('UPDATE comment SET rgt = rgt + 2 WHERE rgt >= %s', [parent_right])
			cursor.execute('UPDATE comment SET lft = lft + 2 WHERE lft >= %s', [parent_right])
			new_left = parent_right
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