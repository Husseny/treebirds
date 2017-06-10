from django.conf.urls import url

from . import views
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^$', views.index),
   url(r'^open_profile/', views.open_profile)
]
