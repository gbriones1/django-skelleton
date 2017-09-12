from django.conf.urls import patterns, include, url
from database import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'provider', views.ProviderViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'employee', views.EmployeeViewSet)
router.register(r'brand', views.BrandViewSet)
router.register(r'appliance', views.ApplianceViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'percentage', views.PercentageViewSet)
router.register(r'organization', views.OrganizationViewSet)
router.register(r'organization_storage', views.OrganizationStorageViewSet)

router.register(r'storage_product', views.StorageProductViewSet)
router.register(r'pricelist', views.PriceListViewSet)
router.register(r'employee_work', views.EmployeeWorkViewSet)

router.register(r'quotation', views.QuotationViewSet)
router.register(r'invoice', views.InvoiceViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'work', views.WorkViewSet)
router.register(r'input', views.InputViewSet)
router.register(r'output', views.OutputViewSet)
router.register(r'lending', views.LendingViewSet)
router.register(r'order', views.OrderViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'^$', views.index),
	url(r'^reports/(?P<name>\W*\w*)$', views.reports),
	url(r'^(?P<name>\w+\W*\w*)/$', views.main),
]
