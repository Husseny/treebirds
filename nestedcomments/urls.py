from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^demo/', views.demo),
	url(r'^add_comment/', views.add_comment),
	url(r'^get_comments/', views.get_comments),
	url(r'^add_nestedcomment/', views.add_nestedcomment)
]