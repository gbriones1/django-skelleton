from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from database.forms import *
from database.models import *
from database.serializers import *

from mysite import graphics
from mysite.email_client import send_email

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

    def create(self, request, *args, **kwargs):
        if request.POST.get('invoice_number'):
            price = float(request.POST.get('invoice_price', 0.0))
            products = json.loads(request.POST.get('products', "[]"))
            if not price:
                price = 0.0
                for p in products:
                    product = Product.objects.get(id=p["id"])
                    price += (float(p["price"]) - (float(p["price"])*float(p["discount"])/100))*int(p["amount"])
            invoice = Invoice.objects.filter(number=request.POST['invoice_number'], date=request.POST['invoice_date'])
            if invoice:
                invoice = invoice[0]
                invoice.price = float(invoice.price) + price
            else:
                provider = None
                if products:
                    provider = Product.object.get(id=products[0]["id"]).provider
                invoice = Invoice(number=request.POST['invoice_number'], date=request.POST['invoice_date'], price=price, provider=provider)
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
        message = message+"\n\nPedido numero: {}\n".format(order.id)
        for p in order.order_product:
            message += "{} {} {}. \tCantidad: {}\n".format(p.product.code, p.product.name, p.product.description, p.amount)
        dest = []
        for pc in order.provider.provider_contact:
            if pc.for_orders and pc.contact.email:
                dest.append(pc.contact.email)
        if dest:
            if send_email(";".join(dest), 'Pedido de productos para Muelles Obrero', message):
                # if send_email('gbriones.gdl@gmail.com;mind.braker@hotmail.com', 'Pedido a '+order.provider.name, message):
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
            'delete': DeleteProductForm,
            'picture': UploadPictureForm,
        },
        'add_fields': [
            ('real_price', 'Precio Real', 'CharField'),
        ],
        'remove_fields': ['price', 'discount'],
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
            ('id', 'Id', 'CharField'),
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
            ('customer_name', 'Customer', 'CharField'),
        ],
        'remove_fields': ['pricelist', 'customer'],
        'filter_form': DateTimeRangeFilterForm(),
        'custom_reg_actions': [
            graphics.Action('mail', 'modal', text='Email', icon='envelope', style='info', method="POST"),
            graphics.Action('work', 'modal', text='Trabajo', icon='wrench', style='info', method="POST"),
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
            'delete': DeleteInvoiceForm,
        },
        'add_fields': [
            ('provider_name', 'Provider', 'CharField'),
        ],
        'remove_fields': ['provider'],
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
            'delete': DeletePaymentForm,
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
            'delete': DeleteSellForm,
        },
        'add_fields': [
            ('customer_name', 'Customer', 'CharField'),
        ],
        'remove_fields': ['customer'],
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
            'delete': DeleteCollectionForm,
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
