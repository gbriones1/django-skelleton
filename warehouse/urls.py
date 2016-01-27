from django.conf.urls import patterns, include, url
from warehouse import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'provider', views.ProviderViewSet)
router.register(r'brand', views.BrandViewSet)
router.register(r'appliance', views.ApplianceViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'organization', views.OrganizationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'^(?P<name>\w+\W*\w*)/$', views.main),
]
