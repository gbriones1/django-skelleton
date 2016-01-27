from django.conf.urls import patterns, include, url
from dashboard import views

urlpatterns = [
	url(r'^$', views.dashboard),
]
