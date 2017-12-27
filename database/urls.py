from django.conf.urls import include, url
from database import views
from rest_framework import routers

router = routers.DefaultRouter()

from database.viewsets import *
router.register(r'provider', ProviderViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'appliance', ApplianceViewSet)
router.register(r'product', ProductViewSet)
router.register(r'percentage', PercentageViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'organization_storage', OrganizationStorageViewSet)

router.register(r'storage_product', StorageProductViewSet)
router.register(r'pricelist', PriceListViewSet)
router.register(r'employee_work', EmployeeWorkViewSet)

router.register(r'quotation', QuotationViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'sell', SellViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'work', WorkViewSet)
router.register(r'input', InputViewSet)
router.register(r'output', OutputViewSet)
router.register(r'lending', LendingViewSet)
router.register(r'order', OrderViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'^special-api/(?P<name>\W*\w*)', views.special_api),
	url(r'^$', views.index),
	url(r'^reports/(?P<name>\W*\w*)$', views.reports),
	url(r'^(?P<name>\w+\W*\w*)/(?P<obj_id>\d*)$', views.main),
]
