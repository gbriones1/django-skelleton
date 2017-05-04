from django.conf.urls import include, url
from settings import views

urlpatterns = [
	url(r'^$', views.main),
]
