# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from user_agents import parse

from models import Activity

import json

from django.http import HttpResponse, JsonResponse

# Create your views here.

def index(request):
	host = request.META['HTTP_HOST'];
	if 'localhost' in host:
		host_name = 'http://'+host+'/'
	else:
		host_name = 'https://'+host+'/'
	save_activity(request, 0)
	return render(request, 'profily/home.html', {host_name: host_name})

def open_profile(request):
	post_data = json.loads(request.body)
	try:
		index = post_data['index']
	except (KeyError):
		return HttpResponse(-1)
	if save_activity(request, index):
		return HttpResponse(1)

def save_activity(request, type):
	ip = get_client_ip(request)
	user_agent_info = request.META['HTTP_USER_AGENT']
	user_agent = parse(user_agent_info)
	browser = user_agent.browser.family
	device = user_agent.device.family
	Activity(ip=ip, browser=browser, device=device, type=type).save()
	return True


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