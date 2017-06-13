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
			cursor.execute('SELECT MAX(rgt) AS max FROM nestedcomments_comment')
			comments = namedtuplefetchall(cursor)
			max_right = comments[0].max
			if max_right == None:
				max_right = 0
			new_left = max_right + 1
			new_right = new_left + 1
			cursor.execute('INSERT INTO nestedcomments_comment (comment, rgt, lft, created_at) VALUES (%s, %s, %s, NOW())',[comment, new_right, new_left])
			result = cursor.lastrowid
			return result

	@classmethod
	def add_nested_comment(cls, parent_comment_id, comment):
		with connection.cursor() as cursor:
			cursor.execute('SELECT rgt as parent_right FROM nestedcomments_comment WHERE id = %s',[parent_comment_id])
			parent_comment = namedtuplefetchall(cursor)
			parent_right = parent_comment[0].parent_right
			cursor.execute('UPDATE nestedcomments_comment SET rgt = rgt + 2 WHERE rgt >= %s', [parent_right])
			cursor.execute('UPDATE nestedcomments_comment SET lft = lft + 2 WHERE lft >= %s', [parent_right])
			new_left = parent_right
			new_right = new_left + 1
			cursor.execute('INSERT INTO nestedcomments_comment (comment, rgt, lft, created_at) VALUES (%s, %s, %s, NOW())',[comment, new_right, new_left])
			result = cursor.lastrowid
			return result

	@classmethod
	def delete_comment(cls, comment_id):
		with connection.cursor() as cursor:
			cursor.execute('SELECT rgt, lft FROM nestedcomments_comment WHERE id = %s',[comment_id])
			comment = namedtuplefetchall(cursor)[0]
			rgt = comment.rgt
			lft = comment.lft
			#Delete comment and its sub comments
			cursor.execute('DELETE FROM nestedcomments_comment where lft >= %s AND lft < %s', [lft, rgt])
			range = rgt - lft + 1

			cursor.execute('UPDATE nestedcomments_comment SET rgt = rgt - %s WHERE rgt > %s',[range, rgt])
			cursor.execute('UPDATE nestedcomments_comment SET lft = lft - %s WHERE lft > %s', [range, rgt])
			return True

	@classmethod
	def view_comments(cls):
		with connection.cursor() as cursor:
			cursor.execute('SELECT node.id, node.comment, FALSE AS show_reply_box, (COUNT(parent.id)) AS depth, CASE WHEN COUNT(parent.id)=1 THEN 0 WHEN COUNT(parent.id)>1 THEN 1 END AS comment_type, FLOOR(HOUR(TIMEDIFF(node.created_at, NOW())) / 24) AS days, MOD(HOUR(TIMEDIFF(node.created_at, NOW())), 24) AS hours, MINUTE(TIMEDIFF(node.created_at, NOW())) AS minutes FROM nestedcomments_comment AS node, nestedcomments_comment AS parent WHERE node.lft BETWEEN parent.lft AND parent.rgt GROUP BY node.id ORDER BY node.lft')
			comments = dictfetchall(cursor)
			for comment in comments:
				days = comment['days']
				hours = comment['hours']
				minutes = comment['minutes']
				time_message = ""
				if days > 0:
					if days>30:
						time_message = "over a month"
					elif days==1:
						time_message = "a day"
					else:
						time_message = str(days)+" days"
				else:
					if hours>0:
						time_message = str(hours)+" hours"
					elif minutes>0:
						time_message = str(minutes)+" minutes"
					else:
						time_message = "a while"
				comment['time_message'] = time_message
			return comments


class User(models.Model):
	name = models.CharField(max_length=30)

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]