from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

import time
import json
import urllib

from database.models import *
from database.forms import *
from database.serializers import *
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
                request.POST._mutable = True
                ids = json.loads(request.POST.get('ids', '[]'))
                for pk in ids:
                    request.POST['id'] = pk
                    vs = object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
                if not ids:
                    notifications.append(Notification(message="No elements selected", level="danger"))
            elif action:
                vs = object_map[name]['viewset'].as_view({'post': action})(request)
            if vs and vs.status_code/100 != 2:
                if hasattr(vs.data, 'iterkeys'):
                    for key in vs.data.keys():
                        notifications.append(Notification(message=str(key)+": "+str(vs.data[key]), level="danger"))
                elif type(vs.data) == type([]):
                    for error in vs.data:
                        notifications.append(Notification(message=str(error), level="danger"))
                else:
                    notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set(cache_name+'-table-update', int(time.time()*1000))
                redirect = request.get_full_path()
                if hasattr(vs, "redirect_to"):
                    redirect = vs.redirect_to
                return HttpResponseRedirect(redirect)
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
def reports(request):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = [
        graphics.Table("reports-table", "Reportes", [("name", "Nombre")], rows=[{"name":"Unidades mas conflictivas"}], checkbox=False, use_cache=False)
    ]
    return render(request, 'pages/database.html', locals())


@login_required
def index(request):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    return render(request, 'pages/database.html', locals())


@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals())


class APIWrapper(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return super(APIWrapper, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(APIWrapper, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(APIWrapper, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # self.serializer = serializer
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super(APIWrapper, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # if getattr(instance, '_prefetched_objects_cache', None):
        #     instance._prefetched_objects_cache = {}
        #
        # return Response(serializer.data)
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

class ProductViewSet(APIWrapper):
    queryset = Product.objects.order_by('code')
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        Provider.objects.get_or_create(name=request.data['provider'])
        Brand.objects.get_or_create(name=request.data['brand'])
        if request.data['appliance']:
            Appliance.objects.get_or_create(name=request.data['appliance'])
        return super(ProductViewSet, self).create(request, *args, **kwargs)

class PercentageViewSet(viewsets.ModelViewSet):
    queryset = Percentage.objects.order_by('max_price_limit')
    serializer_class = PercentageSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.order_by('name')
    serializer_class = OrganizationSerializer

class OrganizationStorageViewSet(APIWrapper):
    queryset = Organization_Storage.objects.order_by('organization')
    serializer_class = OrganizationStorageSerializer


class PriceListViewSet(APIWrapper):
    queryset = PriceList.objects.order_by('customer')
    serializer_class = PriceListSerializer

class StorageProductViewSet(APIWrapper):
    queryset = Storage_Product.objects.order_by('product')
    serializer_class = StorageProductSerializer


class InputViewSet(APIWrapper):
    queryset = Input.objects.order_by('-date')
    serializer_class = InputSerializer

    def create(self, request, *args, **kwargs):
        if request.POST.get('invoice_number'):
            price = float(request.POST.get('invoice_price', 0.0))
            if not price:
                price = 0.0
                for p in json.loads(request.POST.get('products')):
                    product = Product.objects.get(id=p["id"])
                    price += (float(p["price"]) - (float(p["price"])*float(p["discount"])/100))*int(p["amount"])
            invoice = Invoice.objects.filter(number=request.POST['invoice_number'], date=request.POST['invoice_date'])
            if invoice:
                invoice = invoice[0]
                invoice.price = float(invoice.price) + price
            else:
                invoice = Invoice(number=request.POST['invoice_number'], date=request.POST['invoice_date'], price=price)
            invoice.save()
        return super(InputViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        old_invoice = Input.objects.get(id=request.POST["id"]).invoice
        response = super(InputViewSet, self).update(request, *args, **kwargs)
        new_invoice = None
        if request.POST.get('invoice'):
            new_invoice = Invoice.objects.get(id=request.data["invoice"])
            new_invoice.recalculate_price()
        if old_invoice != new_invoice:
            old_invoice.recalculate_price()
        return response

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
        claimant = Employee.objects.filter(id=request.POST.get("claimant") or None)
        claimant = claimant[0] if claimant else None
        organization_storage = Organization_Storage.objects.get(id=request.POST.get("organization_storage"))
        for email_info in provider_map.values():
            order = Order(
                provider=email_info['provider'],
                claimant=claimant,
                organization_storage=organization_storage,
                status=Order.STATUS_PENDING
            )
            order.save()
            for p in email_info["products"]:
                op = Order_Product(order=order, product=p, amount=p.amount)
                op.save()
            email_response = OrderViewSet.send_email(order, request.POST.get('message'))
            if email_response:
                response.append(email_response)
                status = 499
        response = Response(response, status=status)
        response.redirect_to = '/database/order'
        return response

class LendingViewSet(APIWrapper):
    queryset = Lending.objects.order_by('-date')
    serializer_class = LendingSerializer

class OrderViewSet(APIWrapper):
    queryset = Order.objects.order_by('-date')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        result = super(OrderViewSet, self).create(request, *args, **kwargs)
        status = 200
        response = OrderViewSet.send_email(Order.objects.get(id=result.data['id']), request.POST.get('message'))
        if response:
            status = 499
        response = Response([response], status=status)
        return response

    def input(self, request, *args, **kwargs):
        response = InputViewSet.as_view({'post': 'create'})(request)
        if response.status_code/100 == 2:
            response.redirect_to = '/database/input'
            products = json.loads(request._request.POST.get('products', '[]'))
            order = Order.objects.get(id=request._request.POST['order_id'])
            for op in order.order_product:
                for product in products:
                    if op.product.id == product["id"]:
                        op.amount_received = product["amount"]
                        op.save()
                        break
            order.received_date = datetime.now()
            order.save()
        return response

    def mail(self, request, *args, **kwargs):
        status = 200
        response = OrderViewSet.send_email(Order.objects.get(id=request.POST['id']), request.POST.get('message'))
        if response:
            status = 499
        return Response([response], status=status)

    @staticmethod
    def send_email(order, message):
        message = message+"\n\n"
        for p in order.order_product:
            message += "{} {} {}. \tCantidad: {}\n".format(p.product.code, p.product.name, p.product.description, p.amount)
        dest = []
        for pc in order.provider.provider_contact:
            if pc.for_orders and pc.contact.email:
                dest.append(pc.contact.email)
        if dest:
            # if send_email(";".join(dest), 'Pedido de productos para Muelles Obrero', message):
            if send_email('gbriones.gdl@gmail.com;mind.braker@hotmail.com', 'Pedido a '+order.provider.name, message):
                order.status = Order.STATUS_ASKED
                order.save()
            else:
                return "Fallo envio de email a {}".format('gbriones.gdl@gmail.com')
        else:
            return "No se encontraron destinatarios para el proveedor {}".format(order.provider.name)
        return None

class QuotationViewSet(APIWrapper):
    queryset = Quotation.objects.order_by('-date')
    serializer_class = QuotationSerializer

    def mail(self, request, *args, **kwargs):
        response = Response([], status=200)
        return response

    def work(self, request, *args, **kwargs):
        response = Response([], status=200)
        return response

    def output(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        response = OutputViewSet.as_view({'post': 'create'})(request)
        if response.status_code/100 == 2:
            response.redirect_to = '/database/output'
        return response

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
            ('real_price', 'Precio Real', 'CharField'),
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
        'js': ['formset'],
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
        },
        'add_fields': [
            ('contacts', 'Contactos', 'ManyToManyField'),
        ],
        'js': ['formset'],
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
            'new': NewPriceListForm,
            'edit': EditPriceListForm,
            'delete': DeletePriceListForm,
        },
        'add_fields': [
            ('customer_name', 'Customer', 'CharField'),
        ],
        'remove_fields': ['customer'],
        'js': ['multiset', 'pricelist'],
    },
    'storage_product': {
        'name': 'Productos en almacen',
        'api_path': '/database/api/storage_product',
        'use_cache': False,
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
            ('invoice_number', 'Invoice', 'ForeignKey'),
            ('invoice_price', 'Invoice Price', 'CharField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
        ],
        'remove_fields': ['organization_storage', 'invoice'],
        'js': ['multiset', 'input'],
        'filter_form': DateTimeRangeFilterForm()
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
        'filter_form': DateTimeRangeFilterForm()
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
            'input': InputOrderForm,
            'mail': MailOrderForm,
        },
        'add_fields': [
            # ('date', 'Movement Date', 'DateTimeField'),
            ('products', 'Product Set', 'ManyToManyField'),
            ('provider_name', 'Provider', 'CharField'),
            ('claimant_name', 'Claimant', 'CharField'),
            ('organization', 'Organization Name', 'CharField'),
            ('storage', 'Storage Name', 'CharField'),
            ('status', 'Status', 'CharField'),
        ],
        'remove_fields': ['organization_storage', 'provider', 'claimant', 'status'],
        'js': ['multiset', 'order'],
        'custom_reg_actions': [
            graphics.Action('input', 'modal', text='Entrada', icon='sign-in', style='info', method="POST"),
            graphics.Action('mail', 'modal', text='Reenviar', icon='envelope', style='info', method="POST"),
            ],
        'filter_form': DateTimeRangeFilterForm()
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
            'mail': QuotationMailForm,
            'work': QuotationWorkForm,
            'output': QuotationOutputForm,
        },
        'add_fields': [
            ('id', 'Id', 'CharField'),
            ('total', 'Total', 'CharField'),
            ('pricelist_name', 'Pricelist', 'CharField'),
        ],
        'remove_fields': ['pricelist'],
        'filter_form': DateTimeRangeFilterForm(),
        'custom_reg_actions': [
            graphics.Action('mail', 'modal', text='Email', icon='envelope', style='info', method="POST"),
            graphics.Action('work', 'modal', text='Trabajo', icon='wrench', style='info', method="POST"),
            graphics.Action('output', 'modal', text='Salida', icon='sign-out', style='info', method="POST"),
            ],
        'js': ['formset', 'multiset', 'quotation'],
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
