from django.conf.urls import include, url
from public import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^$', views.index),
]
