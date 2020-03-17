from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.utils import IntegrityError

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
import time

object_map = {}

class APIWrapper(viewsets.ModelViewSet):

    def _remove_multiset_cache(self):
        if hasattr(self, 'multiset_caches'):
            multiset_caches = cache.get_many(self.multiset_caches)
            for key in multiset_caches.keys():
                cache.delete(key)

    def list(self, request, *args, **kwargs):
        return super(APIWrapper, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(APIWrapper, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        response = super(APIWrapper, self).destroy(request, *args, **kwargs)
        if int(response.status_code/100) == 2:
            cache.set(self.get_queryset().model.__name__, time.time(), None)
            self._remove_multiset_cache()
        return response

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # self.serializer = serializer
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # import pdb; pdb.set_trace()
        response = super(APIWrapper, self).create(request, *args, **kwargs)
        if int(response.status_code/100) == 2:
            cache.set(self.get_queryset().model.__name__, time.time(), None)
            self._remove_multiset_cache()
        return response

    def update(self, request, *args, **kwargs):
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
        try:
            response = super(APIWrapper, self).update(request, *args, **kwargs)
            if int(response.status_code/100) == 2:
                cache.set(self.get_queryset().model.__name__, time.time(), None)
                self._remove_multiset_cache()
        except IntegrityError as e:
            desc = ""
            if e.args[1].startswith("Duplicate entry"):
                desc = "Valor duplicado: {}".format(" ".join(e.args[1].split(" for ")[0].split()[2:]))
            response = HttpResponseBadRequest(content="Error de integridad en la base de datos: {}".format(desc))
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super(APIWrapper, self).partial_update(request, *args, **kwargs)
        if int(response.status_code/100) == 2:
            cache.set(self.get_queryset().model.__name__, time.time(), None)
            self._remove_multiset_cache()
        return response

    def custom(self, request, *args, **kwargs):
        status = 200
        response = ""
        if response:
            status = 499
        return Response([response], status=status)

    def get_queryset(self):
        return self.queryset.filter(**self.request.query_params.dict())

class ProviderViewSet(APIWrapper):
    queryset = Provider.objects.order_by('name')
    serializer_class = ProviderSerializer

class ProviderContactViewSet(APIWrapper):
    queryset = Provider_Contact.objects.order_by('provider')
    serializer_class = ProviderContactSerializer

class CustomerViewSet(APIWrapper):
    queryset = Customer.objects.order_by('name')
    serializer_class = CustomerSerializer

class CustomerContactViewSet(APIWrapper):
    queryset = Customer_Contact.objects.order_by('customer')
    serializer_class = CustomerContactSerializer

class EmployeeViewSet(APIWrapper):
    queryset = Employee.objects.order_by('name')
    serializer_class = EmployeeSerializer

class BrandViewSet(APIWrapper):
    queryset = Brand.objects.order_by('name')
    serializer_class = BrandSerializer

class ApplianceViewSet(APIWrapper):
    queryset = Appliance.objects.order_by('name')
    serializer_class = ApplianceSerializer

class ProductViewSet(APIWrapper):
    queryset = Product.objects.order_by('code')
    serializer_class = ProductSerializer
    multiset_caches = ['multiset_Quotation_Product', 'multiset_Movement_Product']

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

class PercentageViewSet(APIWrapper):
    queryset = Percentage.objects.order_by('max_price_limit')
    serializer_class = PercentageSerializer

class OrganizationViewSet(APIWrapper):
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

    def create(self, request, *args, **kwargs):
        if request.data.get('action') == 'email':
            return self.email(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)

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
        replacer = Organization.objects.filter(id=request.POST.get("replacer") or None)
        replacer = replacer[0] if replacer else None
        organization_storage = Organization_Storage.objects.get(id=request.POST.get("organization_storage"))
        for email_info in provider_map.values():
            order = Order(
                provider=email_info['provider'],
                claimant=claimant,
                replacer=replacer,
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

    def email(self, request, *args, **kwargs):
        status = 200
        response = OutputViewSet.send_email(Output.objects.filter(id__in=json.loads(request.POST['ids'])), request.POST.get('email'), request.POST.get('message'))
        if response:
            status = 499
        return Response([response], status=status)

    @staticmethod
    def send_email(outputs, email, message):
        total = 0
        for o in outputs:
            message = message+"\n\nSalida numero: {}\tFecha: {}\tAlmacen: {}\n".format(o.id, o.date, o.organization_storage)
            for p in o.movement_product_set.all():
                message += "{} {} {}. \tCantidad: {}\tPrecio unitario: ${}\n".format(p.product.code, p.product.name, p.product.description, p.amount, p.price)
                total += int(p.amount)*float(p.price)
        message += "Total: {}\n".format(total)
        if email:
            config = Configuration.objects.all()
            if config:
                if not settings.DEV_ENV:
                    if not send_email(config[0].sender_email, config[0].password, email, 'Salidas de productos de Muelles Obrero', message):
                        return "Fallo envio de email a {}".format(email)
                else:
                    if not send_email(config[0].sender_email, config[0].password, ['gbriones.gdl@gmail.com', 'mind.braker@hotmail.com'], 'Salidas de productos', message):
                        return "Fallo envio de email a {}".format(email)
            else:
                return "No hay email para enviar pedidos. Ir a Configuracion para establecerlo"
        else:
            return "No se establecio un destinatario"
        return None

# class LendingViewSet(APIWrapper):
#     queryset = Lending.objects.order_by('-date')
#     serializer_class = LendingSerializer

class OrderViewSet(APIWrapper):
    queryset = Order.objects.order_by('-date')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        response = super(OrderViewSet, self).create(request, *args, **kwargs)
        mail_error = None
        config = Configuration.objects.all()
        if config and config[0].sender_email:
            mail_error = OrderViewSet.send_email(Order.objects.get(id=response.data['id']), request.data.get('message'), fail_no_dest=False)
        if mail_error:
            response.status_code = 499
            response.data = {"error": mail_error}
        return response
    
    def update(self, request, *args, **kwargs):
        if request.data.get('action') == 'mail':
            response = Response({}, 201)
            order = Order.objects.get(id=request.data['id'])
            mail_error = None
            mail_error = OrderViewSet.send_email(order, request.data.get('message'))
            if mail_error:
                response.status_code = 499
                response.data = {"error": mail_error}
            return response
        response = super(OrderViewSet, self).update(request, *args, **kwargs)
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
    def send_email(order, message, fail_no_dest=True):
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
                if not settings.DEV_ENV:
                    if send_email(config[0].sender_email, config[0].password, dest, 'Pedido de productos para Muelles Obrero', message):
                        order.status = Order.STATUS_ASKED
                        order.save()
                    else:
                        return "Fallo envio de email a {}".format(dest)
                else:
                    if send_email(config[0].sender_email, config[0].password, ['gbriones.gdl@gmail.com', 'mind.braker@hotmail.com'], 'Pedido a '+order.provider.name, message):
                        order.status = Order.STATUS_ASKED
                        order.save()
                    else:
                        return "Fallo envio de email a {}".format(dest)
            else:
                return "No hay email para enviar pedidos. Ir a Configuracion para establecerlo"
        elif fail_no_dest:
            return "No se encontraron destinatarios para el proveedor {}".format(order.provider.name)
        return None

def render_sheet(request, name, obj_id, instance):
    desc_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_desc', object_map[name].get('table_fields', []))])
    cont_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_cont', [])])
    rest_url = object_map[name]['api_path']
    sheet = graphics.DescriptionSheet(
        name+"-sheet",
        object_map[name].get('sheet_name', object_map[name]['name']),
        obj_id,
        desc_fields=desc_fields,
        cont_fields=cont_fields,
        instance=instance,
        use_rest=rest_url,
    )
    origin = request.META["HTTP_ORIGIN"]
    scripts = ["sheet_quotation"]
    contents = [sheet]
    return render(request, 'pages/quotation.html', locals())

class QuotationViewSet(APIWrapper):
    queryset = Quotation.objects.order_by('-date')
    serializer_class = QuotationSerializer
    
    def update(self, request, *args, **kwargs):
        if request.data.get('action') == 'mail':
            return self.mail(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)

    def mail(self, request, *args, **kwargs):
        status = 500
        response = ''
        quotation = Quotation.objects.get(id=request.POST.get('id'))
        contacts = quotation.customer.customer_contact_set.filter(for_quotation=True)
        if contacts:
            config = Configuration.objects.all()
            if config and config[0].quotations_email:
                rendered = render_sheet(request, 'quotation', quotation.id, quotation)
                origin = request.META["HTTP_ORIGIN"]
                origin = "file:///home/gbriones/Workspace/django-skelleton"
                origin = "file://{}".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                # print(origin)
                html_string = rendered.content.decode().replace('src="/static/', 'src="{}/static/'.format(origin)).replace('href="/static/', 'href="{}/static/'.format(origin))
                html_file = tempfile.mktemp()+".html"
                # print(html_file)
                with open(html_file, "w") as f:
                    f.write(html_string)
                os.chmod(html_file, 438)
                # proc = subprocess.Popen(["xvfb-run", "-a", "-s", '-screen 0 1024x768x16', "wkhtmltopdf", "-q", html_file, "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc = subprocess.Popen(["wkhtmltopdf", "--print-media-type", "-q", html_file, "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                # print(err)
                # pdf_file = tempfile.mktemp()+".pdf"
                # print(pdf_file)
                # with open(pdf_file, "wb") as f:
                #     f.write(out)
                os.remove(html_file)
                if not settings.DEV_ENV:
                    if send_email(config[0].quotations_email, config[0].quotations_password, [contact.email for contact in contacts], request.POST.get('subject', ''), request.POST.get('message', ''), attachments=[{"content":out, "filename":"cotizacion.pdf"}]):
                        status = 200
                        response = "OK"
                    else:
                        response = "Fallo envio de email a {}".format([contact.email for contact in contacts])
                else:
                    if send_email(config[0].quotations_email, config[0].quotations_password, ["gbriones.gdl@gmail.com"], request.POST.get('subject', ''), request.POST.get('message', ''), attachments=[{"content":out, "filename":"cotizacion.pdf"}]):
                        status = 200
                        response = "OK"
                    else:
                        response = "Fallo envio de email a {}".format([contact.email for contact in contacts])
            else:
                response = "No hay email para enviar cotizaciones. Ir a Configuracion para establecerlo"
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
    multiset_caches = ['multiset_Employee_Work']

class ConfigurationViewSet(APIWrapper):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


object_map = {
    'product': {
        'name': 'Refacciones',
        'api_path': '/database/api/product/',
        'prefetch': ['product', 'brand', 'appliance', 'provider'],
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
        'js': ['dashboard', 'product']
    },
    'provider': {
        'name': 'Provedores',
        'api_path': '/database/api/provider/',
        'prefetch': ['provider', 'provider_contact'],
        'model': Provider,
        'viewset': ProviderViewSet,
        'action_forms': {
            'new': NewProviderForm,
            'edit': EditProviderForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_count', 'provider_contact_set'],
        'subset-fields': {'provider_contact_set': ["name", "department", "phone", "email", "for_orders"]},
        'js': ['formset', 'dashboard', 'provider'],
    },
    'customer': {
        'name': 'Clientes',
        'api_path': '/database/api/customer/',
        'prefetch': ['customer', 'customer_contact'],
        'model': Customer,
        'viewset': CustomerViewSet,
        'action_forms': {
            'new': NewCustomerForm,
            'edit': EditCustomerForm,
            'delete': DeleteForm,
            'merge': MergeCustomerForm
        },
        'custom_table_actions': [graphics.Action('merge', 'modal', text='Combinar', icon='compress', style='info', method="")],
        'table_fields': ['name', 'customer_contact_set'],
        'subset-fields': {'customer_contact_set': ["name", "department", "phone", "email"]},
        'js': ['formset', 'dashboard', 'customer'],
    },
    'employee': {
        'name': 'Empleado',
        'api_path': '/database/api/employee/',
        'prefetch': ['employee'],
        'model': Employee,
        'viewset': EmployeeViewSet,
        'action_forms': {
            'new': NewEmployeeForm,
            'edit': EditEmployeeForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name'],
        'js': ['dashboard', 'employee'],
    },
    'brand': {
        'name': 'Marcas',
        'api_path': '/database/api/brand/',
        'prefetch': ['brand'],
        'model': Brand,
        'viewset': BrandViewSet,
        'action_forms': {
            'new': NewBrandForm,
            'edit': EditBrandForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_amount'],
        'js':['dashboard', 'brand']
    },
    'appliance': {
        'name': 'Applicaciones',
        'api_path': '/database/api/appliance/',
        'prefetch': ['appliance'],
        'model': Appliance,
        'viewset': ApplianceViewSet,
        'action_forms': {
            'new': NewApplianceForm,
            'edit': EditApplianceForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name', 'product_amount'],
        'js':['dashboard', 'appliance']
    },
    'percentage': {
        'name': 'Porcentajes',
        'api_path': '/database/api/percentage/',
        'prefetch': ['percentage'],
        'model': Percentage,
        'viewset': PercentageViewSet,
        'action_forms': {
            'new': NewPercentageForm,
            'edit': EditPercentageForm,
            'delete': DeleteForm,
        },
        'table_fields': ['max_price_limit', 'sale_percentage_1', 'sale_percentage_2', 'sale_percentage_3', 'service_percentage_1', 'service_percentage_2', 'service_percentage_3'],
        'js': ['dashboard', 'percentage']
    },
    'organization': {
        'name': 'Organizaciones',
        'api_path': '/database/api/organization/',
        'prefetch': ['organization'],
        'model': Organization,
        'viewset': OrganizationViewSet,
        'action_forms': {
            'new': NewOrganizationForm,
            'edit': EditOrganizationForm,
            'delete': DeleteForm,
        },
        'table_fields': ['name'],
        'js': ['dashboard', 'organization']
    },
    'organization_storage': {
        'name': 'Almacenes',
        'api_path': '/database/api/organization_storage/',
        'prefetch': ['organization_storage'],
        'model': Organization_Storage,
        'viewset': OrganizationStorageViewSet,
        'action_forms': {
            'new': NewOrganizationStorageForm,
            'edit': EditOrganizationStorageForm,
            'delete': DeleteForm,
        },
        'table_fields': ['organization_name', 'storage_type_name'],
        'js': ['dashboard', 'organization_storage']
    },
    'pricelist': {
        'name': 'Listas de precios',
        'api_path': '/database/api/pricelist/',
        'prefetch': ['pricelist'],
        'model': PriceList,
        'viewset': PriceListViewSet,
        'action_forms': {
            'new': NewPriceListForm,
            'edit': EditPriceListForm,
            'delete': DeleteForm,
        },
        'table_fields': ['customer_name',],
        'subset-fields': {'pricelist_product_set': ["product", "price"]},
        'js': ['multiset', 'dashboard', 'pricelist'],
    },
    'storage_product': {
        'name': 'Productos en almacen',
        'api_path': '/database/api/storage_product/',
        'prefetch': ['product', 'organization_storage', 'storage_product'],
        'use_cache': False,
        'model': Storage_Product,
        'viewset': StorageProductViewSet,
        'action_forms': {
            'edit': ChangeStorageProductForm,
            'new': AddStorageProductForm,
        },
        'table_fields': ['product_code', 'product_name', 'product_description', 'product_brand', 'organization_name', 'storage_name', 'amount', 'must_have'],
        'remove_checkbox': True,
        'remove_table_actions': True,
        'custom_table_actions': [graphics.Action('new', 'modal', text='Agregar', icon='plus-circle', style='primary', method="POST")],
        'remove_reg_actions': True,
        'custom_reg_actions': [graphics.Action('edit', 'modal', text='Cambiar', icon='calculator', style='success', method="PUT")],
        'js': ['dashboard', 'storage_product']
    },
    'input': {
        'name': 'Entradas',
        'api_path': '/database/api/input/',
        'prefetch': ['storage_product'],
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
        'js': ['multiset', 'dashboard', 'input'],
        'filter_form': DateTimeRangeFilterForm()
    },
    'output': {
        'name': 'Salidas',
        'api_path': '/database/api/output/',
        'prefetch': ['storage_product'],
        'use_cache': False,
        'model': Output,
        'viewset': OutputViewSet,
        'action_forms': {
            'new': NewOutputForm,
            'edit': EditOutputForm,
            'delete': DeleteForm,
            'order': OrderOutputForm,
            'email': EmailOutputForm,
        },
        'table_fields': ['date', 'movement_product_set', 'employee_name', 'destination_name', 'replacer_name', 'organization_name', 'storage_name'],
        'subset-fields': {'movement_product_set': ["product", "price", "amount"]},
        'js': ['multiset', 'dashboard', 'output'],
        'custom_table_actions': [
            graphics.Action('order', 'modal', text='Pedir', icon='shopping-cart', style='info', method="POST"),
            graphics.Action('email', 'modal', text='Email', icon='envelope', style='info', method="POST")],
        'filter_form': DateTimeRangeFilterForm()
    },
    # 'lending': {
    #     'name': 'Prestamos',
    #     'api_path': '/database/api/lending/',
    #     'use_cache': False,
    #     'model': Lending,
    #     'viewset': LendingViewSet,
    #     'action_forms': {
    #         'new': NewLendingForm,
    #         'edit': EditLendingForm,
    #         'delete': DeleteForm,
    #     },
    #     'table_fields': ['date', 'products', 'organization_name', 'storage_name'],
    #     'js': ['multiset'],
    #     'filter_form': DateRangeFilterForm()
    # },
    'order': {
        'name': 'Pedidos',
        'api_path': '/database/api/order/',
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
        'table_fields': ['id', 'date', 'order_product_set', 'provider_name', 'claimant_name', 'replacer_name', 'organization_name', 'storage_name', 'status'],
        'subset-fields': {'order_product_set': ["product", "amount"]},
        'js': ['multiset', 'dashboard', 'order'],
        'custom_reg_actions': [
            graphics.Action('input', 'modal', text='Entrada', icon='sign-in', style='info', method="POST"),
            graphics.Action('mail', 'modal', text='Reenviar', icon='envelope', style='info', method="POST"),
            ],
        'filter_form': DateTimeRangeFilterForm()
    },
    'quotation': {
        'name': 'Cotizaciones',
        'sheet_name': 'Cotizacion',
        'api_path': '/database/api/quotation/',
        'use_cache': False,
        'model': Quotation,
        'viewset': QuotationViewSet,
        'action_forms': {
            'new': NewQuotationForm,
            'edit': EditQuotationForm,
            'delete': DeleteForm,
            'mail': QuotationMailForm,
            'output': QuotationOutputForm,
            'sell': QuotationSellForm
        },
        'table_fields': ['id', 'date', 'unit', 'plates', 'authorized', 'service', 'discount', 'total', 'customer_name', 'work_sheet'],
        'sheet_desc': ['customer_name', 'unit', 'plates'],
        'sheet_cont': ['quotation_product_set', 'quotation_others_set', 'service', 'discount'],
        'filter_form': DateTimeRangeFilterForm(),
        'custom_reg_actions': [
            graphics.Action('mail', 'modal', text='Email', icon='envelope', style='info', method="POST"),
            # graphics.Action('work', 'modal', text='Trabajo', icon='wrench', style='info', method="POST"),
            graphics.Action('output', 'modal', text='Salida', icon='sign-out', style='info', method="POST"),
            graphics.Action('view', 'navigate', text='Ver', icon='eye', style='info', method="GET"),
            graphics.Action('sell', 'modal', text='Registrar Ingreso', icon='money', style='info', method="POST"),
            ],
        'js': ['formset', 'multiset', 'dashboard', 'quotation'],
    },
    'invoice': {
        'name': 'Gastos',
        'api_path': '/database/api/invoice/',
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
        'js': ['formset', 'dashboard', 'invoice'],
    },
    'sell': {
        'name': 'Ingresos',
        'api_path': '/database/api/sell/',
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
        'js': ['formset', 'dashboard', 'sell'],
    },
    'work': {
        'name': 'Hojas de trabajo',
        'api_path': '/database/api/work/',
        'use_cache': False,
        'model': Work,
        'viewset': WorkViewSet,
        'action_forms': {
            'new': NewWorkForm,
            'edit': EditWorkForm,
            'delete': DeleteForm,
        },
        'filter_form': DateRangeFilterForm(),
        'js': ['multiset', 'dashboard', 'work'],
    },
    'employee_work': {
        'name': 'Comisiones',
        'api_path': '/database/api/employee_work/',
        'use_cache': False,
        'model': Employee_Work,
        'viewset': EmployeeWorkViewSet,
        'action_forms': {
        },
        'filter_form': DateRangeFilterForm()
    }
}
