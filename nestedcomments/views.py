# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Comment
from profily.models import Activity
from user_agents import parse
import json, sys

# Create your views here.

def demo(request):
	ip = get_client_ip(request)
	user_agent_info = request.META['HTTP_USER_AGENT']
	user_agent = parse(user_agent_info)
	browser = user_agent.browser.family
	device = user_agent.device.family
	Activity(ip=ip, browser=browser, device=device, type=5).save()
	host = request.META['HTTP_HOST'];
	if 'localhost' in host:
		host_name = 'http://'+host+'/'
	else:
		host_name = 'https://'+host+'/'
	return render(request, 'nestedcomments/demo.html', {"host_name": host_name})

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

def delete_comment(request):
	post_data = json.loads(request.body)
	try:
		comment_id = post_data['comment_id']
	except (KeyError):
		return HttpResponse(-1)
	result = Comment.delete_comment(comment_id)
	if result:
		return HttpResponse(1)
	else:
		return HttpResponse(-1)

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		print "returning FORWARDED_FOR"
		ip = x_forwarded_for.split(',')[-1].strip()
	elif request.META.get('HTTP_X_REAL_IP'):
		print "returning REAL_IP"
		ip = request.META.get('HTTP_X_REAL_IP')
	else:
		print "returning REMOTE_ADDR"
		ip = request.META.get('REMOTE_ADDR')
	return ip