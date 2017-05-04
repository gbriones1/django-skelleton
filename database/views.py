from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

import time
import json
import urllib

from database.models import (
    Provider, Customer, Employee, Brand, Appliance, Product, Percentage, Organization,
    Organization_Storage, Storage_Product, PriceList, Employee_Work,
    Input, Output, Lending, Order, Quotation, Invoice, Payment, Work,
    Order_Product,
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
    ChangeStorageProductForm,
    OrderOutputForm,
    DateRangeFilterForm
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
from mysite.email_client import send_email

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
        cache_name = name+"-"+urllib.urlencode(request.GET)
        if request.method == 'POST':
            action = request.POST.get('action')
            vs = None
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
            elif action:
                vs = object_map[name]['viewset'].as_view({'post': action})(request)
            if vs and vs.status_code/100 != 2:
                notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set(cache_name+'-table-update', int(time.time()*1000))
                return HttpResponseRedirect(request.get_full_path())
        actions = [] if object_map[name].get('remove_reg_actions') else graphics.Action.edit_and_delete()
        buttons = [] if object_map[name].get('remove_table_actions') else graphics.Action.new_and_multidelete()
        actions.extend(object_map[name].get('custom_reg_actions', []))
        buttons.extend(object_map[name].get('custom_table_actions', []))
        add_fields = object_map[name].get('add_fields', [])
        remove_fields = object_map[name].get('remove_fields', [])
        filter_form = object_map[name].get('filter_form', None)
        use_cache = object_map[name].get('use_cache', True)
        if filter_form:
            if not request.GET:
                filters = {x:y.initial for x,y in filter_form.fields.items()}
                return HttpResponseRedirect(request.get_full_path()+"?"+urllib.urlencode(filters))
            for key in request.GET.keys():
                filter_form.fields[key].initial = request.GET[key]
        checkbox = False if object_map[name].get('remove_checkbox') else True
        rest_url = object_map[name]['api_path']
        if request.GET:
            rest_url += "?"+urllib.urlencode(request.GET)
        table = graphics.Table(
            cache_name+"-table",
            object_map[name]['name'],
            object_map[name]['model'].get_fields(remove_fields=remove_fields, add_fields=add_fields),
            actions=actions,
            buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
            use_rest=rest_url,
            use_cache=use_cache,
            checkbox=checkbox,
        )
        contents = [table]
        for action in actions+buttons:
            content = None
            if action.name in object_map[name]['action_forms'].keys():
                content = object_map[name]['action_forms'][action.name]()
            modal = graphics.Modal.from_action(action, [content])
            contents.append(modal)
        global_messages.append(Message(
            action=cache_name+'-table-update',
            parameter=cache.get_or_set(cache_name+'-table-update', int(time.time()*1000))
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
    def list(self, request, *args, **kwargs):
        return super(APIWrapper, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(APIWrapper, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(APIWrapper, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # obj = get_object_by('viewset', self.__class__)
        # resolve_foreign_fields(request.POST, obj['model'].get_fields())
        return super(APIWrapper, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(APIWrapper, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(APIWrapper, self).partial_update(request, *args, **kwargs)

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        return self.queryset.filter(**self.request.query_params.dict())
        # model_fields = list(map(lambda x: x.name, self.queryset.model._meta.fields))
        # model_filters = {}
        # function_filters = {}
        # for x,y in self.request.query_params.dict().items():
        #     if x in model_fields:
        #         model_filters[x] = y
        #     else:
        #         function_filters[x] = y
        # results = self.queryset.filter(**model_filters)
        # for function_filter in function_filters.keys():
        #     method = function_filter.split("__")
        #     field = method[0]
        #     op = 'eq' if len(method) == 1 else method[1]
        #     if results and hasattr(results[0], field):
        #         if op == 'eq':
        #             results = filter(lambda x:getattr(x, field) == function_filters[function_filter], results)
        #         elif op == 'gt':
        #             results = filter(lambda x:getattr(x, field) > function_filters[function_filter], results)
        #         elif op == 'gte':
        #             results = filter(lambda x:getattr(x, field) >= function_filters[function_filter], results)
        #         elif op == 'lt':
        #             results = filter(lambda x:getattr(x, field) < function_filters[function_filter], results)
        #         elif op == 'lte':
        #             results = filter(lambda x:getattr(x, field) <= function_filters[function_filter], results)
        #         elif op == 'not':
        #             results = filter(lambda x:getattr(x, field) != function_filters[function_filter], results)
        # return results


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


class InputViewSet(APIWrapper):
    queryset = Input.objects.order_by('-date')
    serializer_class = InputSerializer

class OutputViewSet(APIWrapper):
    queryset = Output.objects.order_by('-date')
    serializer_class = OutputSerializer

    def order(self, request, *args, **kwargs):
        provider_map = {}
        for product_info in json.loads(request.POST.get('products', '[]')):
            p = Product.objects.get(id=product_info["id"])
            p.amount = product_info["amount"]
            if p.provider.id in provider_map:
                provider_map[p.provider.id]['products'].append(p)
            else:
                provider_map[p.provider.id] = {
                    'provider': p.provider,
                    'products': [p]
                }
        status = 200
        response = []
        for email_info in provider_map.values():
            message = request.POST.get('message')+"\n\n"
            for p in email_info['products']:
                message += "{} {} {}. \tCantidad: {}\n".format(p.code, p.name, p.description, p.amount)
            dest = []
            for pc in email_info['provider'].provider_contact:
                if pc.for_orders and pc.contact.email:
                    dest.append(pc.contact.email)
            if dest:
                # if send_email(";".join(dest), 'Pedido de productos', message):
                if send_email('gbriones.gdl@gmail.com;mind.braker@hotmail.com', 'Pedido a '+email_info['provider'].name, message):
                    claimant = Employee.objects.filter(id=request.POST.get("claimant") or None)
                    claimant = claimant[0] if claimant else None
                    order = Order(
                        provider=email_info['provider'],
                        claimant=claimant,
                        organization_storage=Organization_Storage.objects.get(id=request.POST.get("organization_storage"))
                    )
                    order.save()
                    for p in email_info["products"]:
                        op = Order_Product(
                            order=order,
                            product=p,
                            amount=p.amount,
                            status=Order.STATUS_ASKED
                        )
                        op.save()
                else:
                    status = 499
                    response.append("Fallo envio de email a {}".format('gbriones.gdl@gmail.com'))
            else:
                status = 498
                response.append("No se encontraron destinatarios para el proveedor {}".format(email_info["provider"].name))
        return Response(response, status=status)

class LendingViewSet(APIWrapper):
    queryset = Lending.objects.order_by('-date')
    serializer_class = LendingSerializer

class OrderViewSet(APIWrapper):
    queryset = Order.objects.order_by('-date')
    serializer_class = OrderSerializer

class QuotationViewSet(APIWrapper):
    queryset = Quotation.objects.order_by('-date')
    serializer_class = QuotationSerializer

class InvoiceViewSet(APIWrapper):
    queryset = Invoice.objects.order_by('-date')
    serializer_class = InvoiceSerializer

class PaymentViewSet(APIWrapper):
    queryset = Payment.objects.order_by('-date')
    serializer_class = PaymentSerializer

class WorkViewSet(APIWrapper):
    queryset = Work.objects.order_by('-date')
    serializer_class = WorkSerializer

class EmployeeWorkViewSet(APIWrapper):
    queryset = Employee_Work.objects.order_by('-work__date')
    serializer_class = EmployeeWorkSerializer

object_map = {
    'product': {
        'name': 'Refacciones',
        'api_path': '/database/api/product',
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
        'model': Provider,
        'viewset': ProviderViewSet,
        'action_forms': {
            'new': NewProviderForm,
            'edit': EditProviderForm,
            'delete': DeleteProviderForm,
        },
        'add_fields': [
            ('product_count', 'Productos', 'IntegerField'),
            ('contacts', 'Contactos', 'ManyToManyField'),
        ],
    },
    'customer': {
        'name': 'Clientes',
        'api_path': '/database/api/customer',
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
        'model': PriceList,
        'viewset': PriceListViewSet,
        'action_forms': {
        }
    },
    'storage_product': {
        'name': 'Productos en almacen',
        'api_path': '/database/api/storage_product',
        'model': Storage_Product,
        'viewset': StorageProductViewSet,
        'action_forms': {
            'edit': ChangeStorageProductForm,
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
        'custom_reg_actions': [graphics.Action('edit', 'modal', text='Cambiar', icon='calculator', style='success', method="POST")],
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
            ('invoice_number', 'Invoice', 'ForeignKey'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage', 'invoice'],
        'js': ['multiset', 'input'],
        'filter_form': DateRangeFilterForm()
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
            'order': OrderOutputForm,
        },
        'add_fields': [
            ('date', 'Movement Date', 'DateTimeField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('employee_name', 'Employee', 'ForeignKey'),
            ('destination_name', 'Destination', 'ForeignKey'),
            ('replacer_name', 'Replacer', 'ForeignKey'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage', 'employee', 'destination', 'replacer'],
        'js': ['multiset', 'output'],
        'custom_reg_actions': [graphics.Action('order', 'modal', text='Pedir', icon='shopping-cart', style='info', method="POST")],
        'filter_form': DateRangeFilterForm()
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
        },
        'add_fields': [
            ('date', 'Movement Date', 'DateTimeField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage'],
        'js': ['multiset'],
        'filter_form': DateRangeFilterForm()
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
        },
        'add_fields': [
            ('date', 'Movement Date', 'DateTimeField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage'],
        'js': ['multiset'],
        'filter_form': DateRangeFilterForm()
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
        },
        'filter_form': DateRangeFilterForm()
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
        },
        'filter_form': DateRangeFilterForm()
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
        },
        'filter_form': DateRangeFilterForm()
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
        },
        'filter_form': DateRangeFilterForm()
    },
    'employee_work': {
        'name': 'Comisiones',
        'api_path': '/database/api/employee_work',
        'use_cache': False,
        'model': Employee_Work,
        'viewset': EmployeeWorkViewSet,
        'action_forms': {
        },
        'filter_form': DateRangeFilterForm()
    }
}