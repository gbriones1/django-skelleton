from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

import time
import json

from database.models import (
    Provider, Customer, Employee, Brand, Appliance, Product, Percentage, Organization,
    Organization_Storage, Storage_Product, PriceList, Employee_Work,
    Input, Output, Lending, Order, Quotation, Invoice, Payment, Work,
)
from database.forms import (
    NewProductForm, EditProductForm, DeleteProductForm,
    NewCustomerForm, EditCustomerForm, DeleteCustomerForm,
    NewEmployeeForm, EditEmployeeForm, DeleteEmployeeForm,
    NewProviderForm, EditProviderForm, DeleteProviderForm,
    NewBrandForm, EditBrandForm, DeleteBrandForm,
    NewApplianceForm, EditApplianceForm, DeleteApplianceForm,
    NewPercentageForm, EditPercentageForm, DeletePercentageForm,
    NewOrganizationForm, EditOrganizationForm, DeleteOrganizationForm,
    NewOrganizationStorageForm, EditOrganizationStorageForm, DeleteOrganizationStorageForm,
    NewInputForm, EditInputForm, DeleteInputForm,
    NewOutputForm, EditOutputForm, DeleteOutputForm,
    NewLendingForm, EditLendingForm, DeleteLendingForm,
    NewOrderForm, EditOrderForm, DeleteOrderForm,
    NewInvoiceForm, EditInvoiceForm, DeleteInvoiceForm,
    NewQuotationForm, EditQuotationForm, DeleteQuotationForm,
    NewPaymentForm, EditPaymentForm, DeletePaymentForm,
    NewWorkForm, EditWorkForm, DeleteWorkForm,
)
from database.serializers import (
    ProviderSerializer, CustomerSerializer, EmployeeSerializer,
    BrandSerializer, ApplianceSerializer, ProductSerializer, PercentageSerializer, OrganizationSerializer,
    OrganizationStorageSerializer, StorageProductSerializer, PriceListSerializer, EmployeeWorkSerializer,
    InputSerializer, OutputSerializer, LendingSerializer, OrderSerializer,
    QuotationSerializer, InvoiceSerializer, PaymentSerializer, WorkSerializer,
)
from mysite import configurations, graphics
from mysite.extensions import Notification, Message

@login_required
def main(request, name):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = []
    notifications = []
    global_messages = []
    scripts = ["tables"]
    if name in object_map.keys():
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'new':
                vs = object_map[name]['viewset'].as_view({'post': 'create'})(request)
            elif action == 'edit':
                request.method = 'PUT'
                vs = object_map[name]['viewset'].as_view({'put': 'update'})(request, pk=request.POST.get('id'))
            elif action == 'delete':
                request.method = 'DELETE'
                vs = object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
            elif action == 'multi-delete':
                request.method = 'DELETE'
                ids = json.loads(request.POST.get('ids', '[]'))
                for pk in ids:
                    vs =  object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
                if not ids:
                    notifications.append(Notification(message="No elements selected", level="danger"))
            if vs and vs.status_code/100 != 2:
                notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set(name+'-table-update', int(time.time()*1000))
                return HttpResponseRedirect(request.get_full_path())
        actions = []
        if not 'remove_reg_actions' in object_map[name] or not object_map[name]['remove_reg_actions']:
            actions = graphics.Action.edit_and_delete()
        buttons = []
        if not 'remove_table_actions' in object_map[name] or not object_map[name]['remove_table_actions']:
            buttons = graphics.Action.new_and_multidelete()
        if 'custom_reg_actions' in object_map[name]:
            actions.extend(object_map[name]['custom_reg_actions'])
        add_fields = object_map[name]['add_fields'] if 'add_fields' in object_map[name] else []
        remove_fields = object_map[name]['remove_fields'] if 'remove_fields' in object_map[name] else []
        checkbox = True
        if 'remove_checkbox' in object_map[name] and object_map[name]['remove_checkbox']:
            checkbox = False
        table = graphics.Table(
            name+"-table",
            object_map[name]['name'],
            object_map[name]['model'].get_fields(remove_fields=remove_fields, add_fields=add_fields),
            actions=actions,
            buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
            use_rest=object_map[name]['api_path'],
            checkbox=checkbox
        )
        contents = [table]
        for action in actions+buttons:
            content = None
            if action.name in object_map[name]['action_forms'].keys():
                content = object_map[name]['action_forms'][action.name]()
            modal = graphics.Modal.from_action(action, [content])
            contents.append(modal)
        global_messages.append(Message(
            action=name+'-table-update',
            parameter=cache.get_or_set(name+'-table-update', int(time.time()*1000))
        ))
        scripts.extend(object_map[name].get('js', []))
    else:
        raise Http404("Page does not exist")
    return render(request, 'pages/database.html', locals())

@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals())


class APIWrapper(viewsets.ModelViewSet):

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # obj = get_object_by('viewset', self.__class__)
        # resolve_foreign_fields(request.POST, obj['model'].get_fields())
        return super(APIWrapper, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(APIWrapper, self).update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super(ProductViewSet, self).update(request, *args, **kwargs)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     return super(ProductViewSet, self).partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(**self.request.query_params.dict())


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.order_by('name')
    serializer_class = ProviderSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.order_by('name')
    serializer_class = CustomerSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.order_by('name')
    serializer_class = EmployeeSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.order_by('name')
    serializer_class = BrandSerializer

class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = Appliance.objects.order_by('name')
    serializer_class = ApplianceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('code')
    serializer_class = ProductSerializer

class PercentageViewSet(viewsets.ModelViewSet):
    queryset = Percentage.objects.order_by('max_price_limit')
    serializer_class = PercentageSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.order_by('name')
    serializer_class = OrganizationSerializer

class OrganizationStorageViewSet(APIWrapper):
    queryset = Organization_Storage.objects.order_by('organization')
    serializer_class = OrganizationStorageSerializer


class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.order_by('customer')
    serializer_class = PriceListSerializer

class StorageProductViewSet(APIWrapper):
    queryset = Storage_Product.objects.order_by('product')
    serializer_class = StorageProductSerializer


class InputViewSet(viewsets.ModelViewSet):
    queryset = Input.objects.order_by('-date')[:500]
    serializer_class = InputSerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.order_by('-date')[:500]
    serializer_class = OutputSerializer

class LendingViewSet(viewsets.ModelViewSet):
    queryset = Lending.objects.order_by('-date')[:500]
    serializer_class = LendingSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-date')[:500]
    serializer_class = OrderSerializer

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.order_by('-date')[:500]
    serializer_class = QuotationSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.order_by('-date')[:500]
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.order_by('-date')[:500]
    serializer_class = PaymentSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.order_by('-date')[:500]
    serializer_class = WorkSerializer

class EmployeeWorkViewSet(viewsets.ModelViewSet):
    queryset = Employee_Work.objects.order_by('-work__date')[:500]
    serializer_class = EmployeeWorkSerializer

object_map = {
    'product': {
        'name': 'Refacciones',
        'api_path': '/database/api/product',
        'use_cache': True,
        'model': Product,
        'viewset': ProductViewSet,
        'action_forms': {
            'new': NewProductForm,
            'edit': EditProductForm,
            'delete': DeleteProductForm,
        },
        'add_fields': [
            ('real_price', 'Real Price', 'CharField'),
            ('percentage_1', 'Percentage 1', 'CharField'),
            ('percentage_2', 'Percentage 2', 'CharField'),
            ('percentage_3', 'Percentage 3', 'CharField'),
        ],
        'remove_fields': ['price', 'discount']
    },
    'provider': {
        'name': 'Provedores',
        'api_path': '/database/api/provider',
        'use_cache': True,
        'model': Provider,
        'viewset': ProviderViewSet,
        'action_forms': {
            'new': NewProviderForm,
            'edit': EditProviderForm,
            'delete': DeleteProviderForm,
        }
    },
    'customer': {
        'name': 'Clientes',
        'api_path': '/database/api/customer',
        'use_cache': True,
        'model': Customer,
        'viewset': CustomerViewSet,
        'action_forms': {
            'new': NewCustomerForm,
            'edit': EditCustomerForm,
            'delete': DeleteCustomerForm,
        }
    },
    'employee': {
        'name': 'Empleado',
        'api_path': '/database/api/employee',
        'use_cache': True,
        'model': Employee,
        'viewset': EmployeeViewSet,
        'action_forms': {
            'new': NewEmployeeForm,
            'edit': EditEmployeeForm,
            'delete': DeleteEmployeeForm,
        }
    },
    'brand': {
        'name': 'Marcas',
        'api_path': '/database/api/brand',
        'use_cache': True,
        'model': Brand,
        'viewset': BrandViewSet,
        'action_forms': {
            'new': NewBrandForm,
            'edit': EditBrandForm,
            'delete': DeleteBrandForm,
        }
    },
    'appliance': {
        'name': 'Applicaciones',
        'api_path': '/database/api/appliance',
        'use_cache': True,
        'model': Appliance,
        'viewset': ApplianceViewSet,
        'action_forms': {
            'new': NewApplianceForm,
            'edit': EditApplianceForm,
            'delete': DeleteApplianceForm,
        }
    },
    'percentage': {
        'name': 'Porcentajes',
        'api_path': '/database/api/percentage',
        'use_cache': True,
        'model': Percentage,
        'viewset': PercentageViewSet,
        'action_forms': {
            'new': NewPercentageForm,
            'edit': EditPercentageForm,
            'delete': DeletePercentageForm,
        }
    },
    'organization': {
        'name': 'Organizaciones',
        'api_path': '/database/api/organization',
        'use_cache': True,
        'model': Organization,
        'viewset': OrganizationViewSet,
        'action_forms': {
            'new': NewOrganizationForm,
            'edit': EditOrganizationForm,
            'delete': DeleteOrganizationForm,
        }
    },
    'organization_storage': {
        'name': 'Almacenes',
        'api_path': '/database/api/organization_storage',
        'use_cache': True,
        'model': Organization_Storage,
        'viewset': OrganizationStorageViewSet,
        'action_forms': {
            'new': NewOrganizationStorageForm,
            'edit': EditOrganizationStorageForm,
            'delete': DeleteOrganizationStorageForm,
        }
    },
    'pricelist': {
        'name': 'Listas de precios',
        'api_path': '/database/api/pricelist',
        'use_cache': True,
        'model': PriceList,
        'viewset': PriceListViewSet,
        'action_forms': {
        }
    },
    'storage_product': {
        'name': 'Productos en almacen',
        'api_path': '/database/api/storage_product',
        'use_cache': True,
        'model': Storage_Product,
        'viewset': StorageProductViewSet,
        'action_forms': {
            # 'edit': EditInputForm,
        },
        'add_fields': [
            ('product_code', 'Product Code', 'CharField'),
            ('product_name', 'Product Name', 'CharField'),
            ('product_description', 'Product Descripcion', 'CharField'),
            ('product_brand', 'Product Brand', 'CharField'),
            ('organization_name', 'Organization Name', 'CharField'),
            ('storage_name', 'Storage Name', 'CharField'),
            ('amount', 'Amount', 'IntegerField'),
            ('must_have', 'Must Have', 'IntegerField'),
        ],
        'remove_fields': ['product', 'organization_storage', 'amount', 'must_have'],
        'remove_checkbox': True,
        'remove_table_actions': True,
        'remove_reg_actions': True,
        'custom_reg_actions': [graphics.Action('change', 'modal', text='Cambiar', icon='calculator', style='success', method="POST")],
    },
    'input': {
        'name': 'Entradas',
        'api_path': '/database/api/input',
        'use_cache': False,
        'model': Input,
        'viewset': InputViewSet,
        'action_forms': {
            'new': NewInputForm,
            'edit': EditInputForm,
            'delete': DeleteInputForm,
        },
        'add_fields': [
            ('date', 'Movement Date', 'DateTimeField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage'],
        'js': ['multiset', 'input']
    },
    'output': {
        'name': 'Salidas',
        'api_path': '/database/api/output',
        'use_cache': False,
        'model': Output,
        'viewset': OutputViewSet,
        'action_forms': {
            'new': NewOutputForm,
            'edit': EditOutputForm,
            'delete': DeleteOutputForm,
        }
    },
    'lending': {
        'name': 'Prestamos',
        'api_path': '/database/api/lending',
        'use_cache': False,
        'model': Lending,
        'viewset': LendingViewSet,
        'action_forms': {
            'new': NewLendingForm,
            'edit': EditLendingForm,
            'delete': DeleteLendingForm,
        }
    },
    'order': {
        'name': 'Pedidos',
        'api_path': '/database/api/order',
        'use_cache': False,
        'model': Order,
        'viewset': OrderViewSet,
        'action_forms': {
            'new': NewOrderForm,
            'edit': EditOrderForm,
            'delete': DeleteOrderForm,
        }
    },
    'quotation': {
        'name': 'Cotizaciones',
        'api_path': '/database/api/quotation',
        'use_cache': False,
        'model': Quotation,
        'viewset': QuotationViewSet,
        'action_forms': {
            'new': NewQuotationForm,
            'edit': EditQuotationForm,
            'delete': DeleteQuotationForm,
        }
    },
    'invoice': {
        'name': 'Facturas de compras',
        'api_path': '/database/api/invoice',
        'use_cache': False,
        'model': Invoice,
        'viewset': InvoiceViewSet,
        'action_forms': {
            'new': NewInvoiceForm,
            'edit': EditInvoiceForm,
            'delete': DeleteInvoiceForm,
        }
    },
    'payment': {
        'name': 'Pagos',
        'api_path': '/database/api/payment',
        'use_cache': False,
        'model': Payment,
        'viewset': PaymentViewSet,
        'action_forms': {
            'new': NewPaymentForm,
            'edit': EditPaymentForm,
            'delete': DeletePaymentForm,
        }
    },
    'work': {
        'name': 'Hojas de trabajo',
        'api_path': '/database/api/work',
        'use_cache': False,
        'model': Work,
        'viewset': WorkViewSet,
        'action_forms': {
            'new': NewWorkForm,
            'edit': EditWorkForm,
            'delete': DeleteWorkForm,
        }
    },
    'employee_work': {
        'name': 'Comisiones',
        'api_path': '/database/api/employee_work',
        'use_cache': False,
        'model': Employee_Work,
        'viewset': EmployeeWorkViewSet,
        'action_forms': {
        }
    }
}
