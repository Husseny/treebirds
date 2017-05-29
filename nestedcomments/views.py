# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def demo(request):
	return render(request, 'nestedcomments/demo.html', {})