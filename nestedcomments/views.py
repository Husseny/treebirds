# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Comment
import json, sys

# Create your views here.

def demo(request):
	return render(request, 'nestedcomments/demo.html', {})

def add_comment(request):
	post_data = json.loads(request.body)
	try:
		comment = post_data['comment']
	except (KeyError):
		return HttpResponse(-1)
	result = Comment.add_comment(comment)
	return HttpResponse(result)

def add_nestedcomment(request):
	post_data = json.loads(request.body)
	try:
		comment = post_data['comment']
		parent_id = post_data['parent_id']
	except (KeyError):
		return HttpResponse(-1)
	result = Comment.add_nested_comment(parent_id, comment)
	return HttpResponse(result)

def get_comments(request):
	result = Comment.view_comments()
	return JsonResponse(json.dumps(result), safe=False)