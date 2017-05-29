from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^demo/', views.demo),
	url(r'^add_comment/', views.add_comment)
]