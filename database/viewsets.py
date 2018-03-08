from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from database.forms import *
from database.models import *
from database.serializers import *

from mysite import graphics
from mysite import configurations
from mysite import settings
from mysite.email_client import send_email

import urllib
import os
import subprocess
import tempfile

object_map = {}

class APIWrapper(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return super(APIWrapper, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(APIWrapper, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(APIWrapper, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
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

    def custom(self, request, *args, **kwargs):
        status = 200
        response = ""
        if response:
            status = 499
        return Response([response], status=status)

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

class ProductViewSet(APIWrapper):
    queryset = Product.objects.order_by('code')
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if not request.POST:
            request = request._stream
            for field in request.FILES.keys():
                request.POST[field] = request.FILES[field]
            request.data = request.POST
        Provider.objects.get_or_create(name=request.POST['provider'])
        Brand.objects.get_or_create(name=request.POST['brand'])
        if request.POST['appliance']:
            Appliance.objects.get_or_create(name=request.POST['appliance'])
        return super(ProductViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.POST:
            request = request._stream
            for field in request.FILES.keys():
                request.POST[field] = request.FILES[field]
            request.data = request.POST
        Provider.objects.get_or_create(name=request.POST['provider'])
        Brand.objects.get_or_create(name=request.POST['brand'])
        if request.POST['appliance']:
            Appliance.objects.get_or_create(name=request.POST['appliance'])
        return super(ProductViewSet, self).update(request, *args, **kwargs)

    def picture(self, request, *args, **kwargs):
        if not request.POST:
            request = request._stream
            for field in request.FILES.keys():
                request.POST[field] = request.FILES[field]
            request.data = request.POST
        product = Product.objects.get(id=request.data.get("id"))
        product.picture = request.data.get('picture')
        product.save()
        return Response([""], status=200)

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

class OutputViewSet(APIWrapper):
    queryset = Output.objects.order_by('-date')
    serializer_class = OutputSerializer

    def order(self, request, *args, **kwargs):
        provider_map = {}
        for product_info in json.loads(request.POST.get('order_product_set', '[]')):
            p = Product.objects.get(id=product_info["product"])
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
            # response.redirect_to = '/database/input'
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
        message = message+"\n\nPedido numero: {}\n".format(order.id)
        for p in order.order_product:
            message += "{} {} {}. \tCantidad: {}\n".format(p.product.code, p.product.name, p.product.description, p.amount)
        dest = []
        for pc in order.provider.provider_contact_set.all():
            if pc.for_orders and pc.email:
                dest.append(pc.email)
        if dest:
            config = Configuration.objects.all()
            if config:
                # if send_email(config[0].sender_email, config[0].password, dest, 'Pedido de productos para Muelles Obrero', message):
                if send_email(config[0].sender_email, config[0].password, ['gbriones.gdl@gmail.com', 'mind.braker@hotmail.com'], 'Pedido a '+order.provider.name, message):
                    order.status = Order.STATUS_ASKED
                    order.save()
                else:
                    return "Fallo envio de email a {}".format(dest)
            else:
                return "No hay email para enviar pedidos. Ir a Configuracion para establecerlo"
        else:
            return "No se encontraron destinatarios para el proveedor {}".format(order.provider.name)
        return None

def render_sheet(request, name, obj_id, instance):
    desc_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_desc', object_map[name].get('table_fields', []))])
    cont_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_cont', [])])
    sheet = graphics.DescriptionSheet(
        name+"-sheet",
        object_map[name].get('sheet_name', object_map[name]['name']),
        obj_id,
        desc_fields=desc_fields,
        cont_fields=cont_fields,
        instance=instance
    )
    contents = [sheet]
    return render(request, 'pages/sheet.html', locals())

class QuotationViewSet(APIWrapper):
    queryset = Quotation.objects.order_by('-date')
    serializer_class = QuotationSerializer

    def mail(self, request, *args, **kwargs):
        status = 500
        response = ''
        quotation = Quotation.objects.get(id=request.POST.get('id'))
        contacts = quotation.customer.customer_contact_set.filter(for_quotation=True)
        if contacts:
            config = Configuration.objects.all()
            if config:
                rendered = render_sheet(request, 'quotation', quotation.id, quotation)
                html_string = rendered.content.replace('src=/static/', 'src={}/static/'.format(request.META["HTTP_ORIGIN"])).replace('href=/static/', 'href={}/static/'.format(request.META["HTTP_ORIGIN"]))
                html_file = tempfile.mktemp()+".html"
                with open(html_file, "w") as f:
                    f.write(html_string)
                os.chmod(html_file, 438)
                proc = subprocess.Popen(["xvfb-run", "-a", "-s", '-screen 0 1024x768x16', "wkhtmltopdf", "-q", html_file, "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                os.remove(html_file)
                if send_email(config[0].quotations_email, config[0].quotations_password, [contact.email for contact in contacts], request.POST.get('subject', ''), request.POST.get('message', ''), attachments=[{"content":out, "filename":"cotizacion.pdf"}]):
                    # if send_email(config[0].quotations_email, config[0].quotations_password, ["gbriones.gdl@gmail.com"], request.POST.get('subject', ''), request.POST.get('message', ''), attachments=[{"content":out, "filename":"cotizacion.pdf"}]):
                    status = 200
                    response = "OK"
                else:
                    response = "Fallo envio de email a {}".format([contact.email for contact in contacts])
            else:
                return "No hay email para enviar cotizaciones. Ir a Configuracion para establecerlo"
        else:
            response =  "No se encontraron destinatarios para el cliente {}".format(quotation.customer.name)
        response = Response([response], status=status)
        return response

    def work(self, request, *args, **kwargs):
        response = Response([], status=200)
        return response

    def output(self, request, *args, **kwargs):
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

class SellViewSet(APIWrapper):
    queryset = Sell.objects.order_by('-date')
    serializer_class = SellSerializer

class CollectionViewSet(APIWrapper):
    queryset = Collection.objects.order_by('-date')
    serializer_class = CollectionSerializer

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
            'delete': DeleteForm,
            'picture': UploadPictureForm,
        },
        'table_fields': ['code', 'provider_name', 'brand_name', 'name', 'description', 'appliance_name', 'real_price', 'percentage_1', 'percentage_2', 'percentage_3', 'picture'],
        'custom_reg_actions': [graphics.Action('picture', 'modal', text='Cargar foto', icon='camera', style='info', method="POST")],
        'js': ['product']
    },
    'provider': {
        'name': 'Provedores',
        'api_path': '/database/api/provider',
        'model': Provider,
        'viewset': ProviderViewSet,
        'action_forms': {
            'new': NewProviderForm,
            'edit': EditProviderForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_count', 'provider_contact_set'],
        'subset-fields': {'provider_contact_set': ["name", "department", "phone", "email", "for_orders"]},
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
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'customer_contact_set'],
        'subset-fields': {'customer_contact_set': ["name", "department", "phone", "email"]},
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
            'delete': DeleteForm,
        },
        'table_fields': ['name'],
    },
    'brand': {
        'name': 'Marcas',
        'api_path': '/database/api/brand',
        'model': Brand,
        'viewset': BrandViewSet,
        'action_forms': {
            'new': NewBrandForm,
            'edit': EditBrandForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_amount'],
    },
    'appliance': {
        'name': 'Applicaciones',
        'api_path': '/database/api/appliance',
        'model': Appliance,
        'viewset': ApplianceViewSet,
        'action_forms': {
            'new': NewApplianceForm,
            'edit': EditApplianceForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_amount'],
    },
    'percentage': {
        'name': 'Porcentajes',
        'api_path': '/database/api/percentage',
        'model': Percentage,
        'viewset': PercentageViewSet,
        'action_forms': {
            'new': NewPercentageForm,
            'edit': EditPercentageForm,
            'delete': DeleteForm,
        },
        'table_fields': ['max_price_limit', 'sale_percentage_1', 'sale_percentage_2', 'sale_percentage_3', 'service_percentage_1', 'service_percentage_2', 'service_percentage_3'],
    },
    'organization': {
        'name': 'Organizaciones',
        'api_path': '/database/api/organization',
        'model': Organization,
        'viewset': OrganizationViewSet,
        'action_forms': {
            'new': NewOrganizationForm,
            'edit': EditOrganizationForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name'],
    },
    'organization_storage': {
        'name': 'Almacenes',
        'api_path': '/database/api/organization_storage',
        'model': Organization_Storage,
        'viewset': OrganizationStorageViewSet,
        'action_forms': {
            'new': NewOrganizationStorageForm,
            'edit': EditOrganizationStorageForm,
            'delete': DeleteForm,
        },
        'table_fields': ['organization_name', 'storage_type_name'],
    },
    'pricelist': {
        'name': 'Listas de precios',
        'api_path': '/database/api/pricelist',
        'model': PriceList,
        'viewset': PriceListViewSet,
        'action_forms': {
            'new': NewPriceListForm,
            'edit': EditPriceListForm,
            'delete': DeleteForm,
        },
        'table_fields': ['customer_name',],
        'subset-fields': {'pricelist_product_set': ["product", "price"]},
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
        'table_fields': ['product_code', 'product_name', 'product_description', 'product_brand', 'organization_name', 'storage_name', 'amount', 'must_have'],
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
            'delete': DeleteForm,
        },
        'table_fields': ['date', 'invoice_number', 'invoice_price', 'movement_product_set', 'organization_name', 'storage_name'],
        'subset-fields': {'movement_product_set': ["product", "price", "amount"]},
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
            'delete': DeleteForm,
            'order': OrderOutputForm,
        },
        'table_fields': ['date', 'movement_product_set', 'employee_name', 'destination_name', 'replacer_name', 'organization_name', 'storage_name'],
        'subset-fields': {'movement_product_set': ["product", "price", "amount"]},
        'js': ['multiset', 'output'],
        'custom_table_actions': [graphics.Action('order', 'modal', text='Pedir', icon='shopping-cart', style='info', method="POST")],
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
            'delete': DeleteForm,
        },
        'table_fields': ['date', 'products', 'organization_name', 'storage_name'],
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
            'delete': DeleteForm,
            'input': InputOrderForm,
            'mail': MailOrderForm,
        },
        'table_fields': ['id', 'date', 'order_product_set', 'provider_name', 'claimant_name', 'organization_name', 'storage_name', 'status'],
        'subset-fields': {'order_product_set': ["product", "amount"]},
        'js': ['multiset', 'order'],
        'custom_reg_actions': [
            graphics.Action('input', 'modal', text='Entrada', icon='sign-in', style='info', method="POST"),
            graphics.Action('mail', 'modal', text='Reenviar', icon='envelope', style='info', method="POST"),
            ],
        'filter_form': DateTimeRangeFilterForm()
    },
    'quotation': {
        'name': 'Cotizaciones',
        'sheet_name': 'Cotizacion',
        'api_path': '/database/api/quotation',
        'use_cache': False,
        'model': Quotation,
        'viewset': QuotationViewSet,
        'action_forms': {
            'new': NewQuotationForm,
            'edit': EditQuotationForm,
            'delete': DeleteForm,
            'mail': QuotationMailForm,
            # 'work': QuotationWorkForm,
            'output': QuotationOutputForm,
        },
        'table_fields': ['id', 'date', 'unit', 'plates', 'authorized', 'service', 'discount', 'total', 'customer_name', 'work_sheet'],
        'sheet_desc': ['customer_name', 'unit', 'plates', 'work_sheet'],
        'sheet_cont': ['quotation_product_set', 'quotation_others_set', 'service', 'discount'],
        'filter_form': DateTimeRangeFilterForm(),
        'custom_reg_actions': [
            graphics.Action('mail', 'modal', text='Email', icon='envelope', style='info', method="POST"),
            # graphics.Action('work', 'modal', text='Trabajo', icon='wrench', style='info', method="POST"),
            graphics.Action('output', 'modal', text='Salida', icon='sign-out', style='info', method="POST"),
            graphics.Action('view', 'navigate', text='Ver', icon='eye', style='info', method="GET"),
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
            'delete': DeleteForm,
        },
        'table_fields': ['date', 'number', 'provider_name', 'payment_set', 'price', 'due', 'paid'],
        'subset-fields': {'payment_set': ["date", "amount"]},
        'filter_form': DateRangeFilterForm(),
        'js': ['formset'],
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
            'delete': DeleteForm,
        },
        'filter_form': DateRangeFilterForm()
    },
    'sell': {
        'name': 'Facturas de ventas',
        'api_path': '/database/api/sell',
        'use_cache': False,
        'model': Sell,
        'viewset': SellViewSet,
        'action_forms': {
            'new': NewSellForm,
            'edit': EditSellForm,
            'delete': DeleteForm,
        },
        'table_fields': ['date', 'number', 'customer_name', 'collection_set', 'price', 'due', 'paid'],
        'subset-fields': {'collection_set': ["date", "amount"]},
        'filter_form': DateRangeFilterForm(),
        'js': ['formset'],
    },
    'collection': {
        'name': 'Cobros',
        'api_path': '/database/api/collection',
        'use_cache': False,
        'model': Collection,
        'viewset': CollectionViewSet,
        'action_forms': {
            'new': NewCollectionForm,
            'edit': EditCollectionForm,
            'delete': DeleteForm,
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
            'delete': DeleteForm,
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
