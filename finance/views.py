# from re import S

from xml.dom.minidom import Document
from rest_framework.response import Response
from django.views.generic import TemplateView
from .task import test_celery
from tenant.models import Lease
from customAuth.serializers import PayeeSerializers,Payee
from communications.utils import Util
from communications.models import Email
from .models import Charges, Expense,Invoice,Receipt, Statement,Payment_options
from property.models import Unit
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from utils.bulk_insert import bulk_data_fomart,bulk_data_fomart_receipt
from .utils import generate_transaction_id
from django.db.models import Sum,OuterRef, Subquery,F,Q
from .serializers import ChargeSerializers,InvoiceSerializers,ReceiptSerializers,ExpenseSerializers,PaymentOptionsSerializers
from utils import custom_apiviews,error_loop,html_pdf
import json,datetime,uuid
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import HttpResponse
from django.views.generic import View

from django.template.loader import get_template

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.conf import settings
# import datetime





# class dashboard(TemplateView):
    
#     template_name = "property/dashboard.html"
    
class receipt(TemplateView):
    
    template_name = "finance/receipt.html"
    
class invoice(TemplateView):
    
    template_name = "finance/invoice.html"
class creditnote(TemplateView):
    
    template_name = "finance/creditnote.html"
class debitnote(TemplateView):
    
    template_name = "finance/debitnote.html"
class balances(TemplateView):
    
    template_name = "finance/balances.html"

class payee(TemplateView):
    
    template_name = "finance/payee.html"
class expenses(TemplateView):
    
    template_name = "finance/expenses.html"
class expense_payments(TemplateView):
    
    template_name = "finance/expense_payments.html"
class payment_options(TemplateView):
    
    template_name = "finance/payment_options.html"
# class income_summary(TemplateView):
    
#     template_name = "finance/income_summary.html"

# class statements(TemplateView):
    
#     template_name = "finance/statements.html"
def auto_invoice_schedule():


	print("------------------")
class invoice_pdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template("finance/invoice_document.html")
        context = {}
        invoice =Invoice.objects.filter(invoice_group__statement_invoice=self.kwargs.get('invoice')).order_by('-created_on').select_related("invoice_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')
        payment_options=Payment_options.objects.filter(property=invoice[0].lease.unit.unit_property)
        context['invoice'] =invoice
        context['payment_options'] =payment_options
        context['unit']=invoice[0].lease.unit.unit_name
        context['invoice_type']=invoice[0].invoice_type
        context['created_on']=invoice[0].created_on.strftime("%d %b, %Y")
        context['statement_invoice']=invoice[0].invoice_group.statement_invoice
        context['property']=invoice[0].lease.unit.unit_property.property_name
        context['city']=invoice[0].lease.unit.unit_property.city
        context['country']=invoice[0].lease.unit.unit_property.country
        context['tenant']=invoice[0].lease.tenant.name
        context['phone']=invoice[0].lease.tenant.phone_number
        context['email']=invoice[0].lease.tenant.email
        context['added_by_email']=invoice[0].added_by.email
        context['calling_code']=invoice[0].lease.tenant.calling_code
        context['late_fee']=invoice[0].late_fee
        context['late_fee_date']=invoice[0].late_fee_date
        context['description']=invoice[0].description
        context['name']=invoice[0].name
        html = template.render(context)
        pdf = html_pdf.render_to_pdf("finance/invoice_pdf.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
class receipt_pdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template("finance/receipt_document.html")
        context = {}
        receipt =Receipt.objects.filter(receipt_group__statement_receipt=self.kwargs.get('receipt')).order_by('-created_on').select_related("receipt_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')[:1]
        context['receipt'] =receipt
        context['unit']=receipt[0].lease.unit.unit_name
        context['receipt_type']=receipt[0].receipt_type
        context['created_on']=receipt[0].created_on.strftime("%d %b, %Y")
        context['statement_receipt']=receipt[0].receipt_group.statement_receipt
        context['property']=receipt[0].lease.unit.unit_property.property_name
        context['city']=receipt[0].lease.unit.unit_property.city
        context['country']=receipt[0].lease.unit.unit_property.country
        context['tenant']=receipt[0].lease.tenant.name
        context['phone']=receipt[0].lease.tenant.phone_number
        context['email']=receipt[0].lease.tenant.email
        context['added_by_email']=receipt[0].added_by.email
        context['calling_code']=receipt[0].lease.tenant.calling_code
        context['description']=receipt[0].description
        context['paid_through']=receipt[0].paid_through
        context['amount']=receipt[0].receipt_group.amount
   
    
        html = template.render(context)
        pdf = html_pdf.render_to_pdf("finance/receipt_pdf.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class invoice_document(TemplateView):
    
    template_name = "finance/invoice_document.html"
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # context['property'] = get_object_or_404(Property, pk=self.kwargs.get('property'))
            invoice =Invoice.objects.filter(invoice_group__statement_invoice=self.kwargs.get('invoice')).order_by('-created_on').select_related("invoice_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')
            payment_options=Payment_options.objects.filter(property=invoice[0].lease.unit.unit_property)
            context['invoice'] =invoice
            context['payment_options'] =payment_options
            context['invoice_type']=invoice[0].invoice_type
            context['unit']=invoice[0].lease.unit.unit_name
            context['created_on']=invoice[0].created_on.strftime("%d %b, %Y")
            context['statement_invoice']=invoice[0].invoice_group.statement_invoice
            context['property']=invoice[0].lease.unit.unit_property.property_name
            context['city']=invoice[0].lease.unit.unit_property.city
            context['country']=invoice[0].lease.unit.unit_property.country
            context['tenant']=invoice[0].lease.tenant.name
            context['phone']=invoice[0].lease.tenant.phone_number
            context['email']=invoice[0].lease.tenant.email
            context['added_by_email']=invoice[0].added_by.email
            context['calling_code']=invoice[0].lease.tenant.calling_code
            context['late_fee']=invoice[0].late_fee
            context['late_fee_date']=invoice[0].late_fee_date
            context['description']=invoice[0].description
            context['name']=invoice[0].name
            context['name']=invoice[0].name
            return context
class receipt_document(TemplateView):
    
    template_name = "finance/receipt_document.html"
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            receipt =Receipt.objects.filter(receipt_group__statement_receipt=self.kwargs.get('receipt')).order_by('-created_on').select_related("receipt_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')[:1]
            context['receipt'] =receipt
            context['receipt_type']=receipt[0].receipt_type
            context['unit']=receipt[0].lease.unit.unit_name
            context['created_on']=receipt[0].created_on.strftime("%d %b, %Y")
            context['statement_receipt']=receipt[0].receipt_group.statement_receipt
            context['property']=receipt[0].lease.unit.unit_property.property_name
            context['city']=receipt[0].lease.unit.unit_property.city
            context['country']=receipt[0].lease.unit.unit_property.country
            context['tenant']=receipt[0].lease.tenant.name
            context['phone']=receipt[0].lease.tenant.phone_number
            context['email']=receipt[0].lease.tenant.email
            context['added_by_email']=receipt[0].added_by.email
            context['calling_code']=receipt[0].lease.tenant.calling_code
            context['description']=receipt[0].description
            context['paid_through']=receipt[0].paid_through
            context['amount']=receipt[0].receipt_group.amount
   
            return context

    
class EditDelete_charges(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = ChargeSerializers
    queryset = Charges.objects.all()
    success_update='The charge was updated'
    success_delete='The charge was deleted'

    def get_queryset(self):
        return Charges.objects.all()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        action=request.POST.get('action')   
        charge_id=request.POST.get('id')   
        id_list=request.POST.get('id_list').split(",")
        property_create_number=request.POST.get('property_create_number')   
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   
      
        print("unitttttttt",unit_create_numbers)
        print("prooop",property_create_number)
        print("acccccccction",action)
        if action=="update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        else:
            many=False
            serializer = self.get_serializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            if action !="update":
                print("previos id list",id_list)
                new_id= serializer.data['id']
                id_list.remove(charge_id)
                id_list.append(new_id)
                unit_create_numbers=[int(i) for i in unit_create_numbers]
                print("Now id list",id_list)
                print("Now unit",unit_create_numbers)
                data=Unit.objects.filter(create_nos__in=unit_create_numbers)
                print(data)

                Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
                unit_charges=id_list)

                
            return Response({
                'success': self.success_update,
                'response': serializer.data,
                'id_list': id_list,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        action=request.POST.get('action')   
        charge_id=request.POST.get('charge_id')   
        id_list=request.POST.get('id_list').split(",")
        property_create_number=request.POST.get('property_create_number') 
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",") 
        print("chargeeeeeeeee id",charge_id)  
        print("uni cret",unit_create_numbers)
        print("uni cret",unit_create_numbers)
        if action=="update":
            self.perform_destroy(instance)
        
        id_list.remove(charge_id)
        Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
            unit_charges=id_list)
        return Response({
                'id_list': id_list,
                'success': self.success_delete,
                # 'status':status.HTTP_204_NO_CONTENT
            })

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_charges(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Charges.objects.all()
    serializer_class = ChargeSerializers
    success_insert='Your charge has been added'
    def create(self, request, format=None, *args, **kwargs):
        property_create_number=request.POST.get('property_create_number') 
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   
  
        id_list=request.POST.get('id_list').split(",") 
 
            
            
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():

            saved_user2 = serializer.save(added_by=self.request.user)
            charge_id= serializer.data['id']
            id_list=list(filter(None, id_list))

            id_list.append(charge_id)
            Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
             unit_charges=id_list)
        
         
            return Response({
                'charge_id': charge_id,
                'id_list': id_list,
            
                'success': self.success_insert,
                # 'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        id_list=json.loads(self.request.query_params.get('data_table'))
        if id_list:
            id_list=[int(i) for i in id_list]
        else:
            id_list=[]
        data=Charges.objects.filter(id__in=id_list).order_by('duration')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name','amount', 'duration')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        data = []
        row_data = filtered_queryset
        for row in row_data:
           data.append ([
                row.duration,
                row.name,
                row.amount,
                row.notify,
               f''' 
                <div class="dropdown float-right">
                    <button type="button"
                        class="btn btn-primary light sharp btn-rounded"
                        data-toggle="dropdown" aria-expanded="false">
                        <svg width="20px" height="20px" viewBox="0 0 24 24"
                            version="1.1">
                            <g stroke="none" stroke-width="1" fill="none"
                                fill-rule="evenodd">
                                <rect x="0" y="0" width="24" height="24"></rect>
                                <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                            </g>
                        </svg>
                    </button>
                    <div class="dropdown-menu" x-placement="bottom-start"
                        style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                      
                        <a class="dropdown-item edit_charges_button text-primary" id="{row.id}">Edit</a>
                        <a class="dropdown-item delete_charges_button text-primary" id="{row.name},{row.id},{row.created_at}">Delete</a>
                    </div>
                </div>
               ''',
                
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)
    

        


class EditDelete_invoice(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = InvoiceSerializers
    queryset = Invoice.objects.all()
    success_update='The Invoice was updated'
    success_delete='The Invoice was deleted'

    def get_queryset(self):
        return Invoice.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_invoice(custom_apiviews.ListBulkCreateAPIView):

    # SELECT "finance_invoice"."invoice_group_id", COUNT("finance_invoice"."invoice_group_id") AS "ni" FROM "finance_invoice" GROUP BY "finance_invoice"."invoice_group_id"

    data = []
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers
    success_insert='Your invoice has been added'
    def create(self, request, format=None, *args, **kwargs):
        success_insert=self.success_insert
        unit_list=request.POST.get('unit_list').split(",") 
        unit_list=[int(i) for i in unit_list]
        statement=str(uuid.uuid4()).replace("-","").upper()
        communication=request.POST.get('communication')
        request.data._mutable = True

        invoice_group_bulk=generate_transaction_id()
        request.data['invoice_group_bulk']=invoice_group_bulk

        raw_data=bulk_data_fomart(request.data)
        many = isinstance(raw_data, list)
        serializer = self.get_serializer(data=raw_data, many=many)
        leases=Lease.objects.filter(id__in=unit_list)
    
        if serializer.is_valid():
            data=serializer.data
            created_on=datetime.datetime.now()
            for row in leases:
                lease=row
                lease_title=row.id
                total_amount=0
                invoice_group=f'INV{lease_title}{invoice_group_bulk}'
                # print("-------------------------",lease_title,"eeeeeee",invoice_group)
                instance=Statement.objects.create(statement_invoice=invoice_group,lease=lease,type='invoice',amount=total_amount,created_on=created_on,added_by=self.request.user)
                # statement_instance=instance.statement_invoice
                for child_row in data:
                    print("==============================================")
                    print(child_row)
                    child_row['lease']=lease
                    total_amount+=int(child_row['amount'])
                    if child_row['late_fee_amount'] > 0:
                        child_row['deadline_date'] = datetime.date.today() + datetime.timedelta(days=child_row['late_fee_grace'])
                    Invoice.objects.create(added_on=child_row['added_on']
                    ,lease=child_row['lease']
                    ,invoice_group=instance,invoice_group_bulk=child_row['invoice_group_bulk']
                   ,name=child_row['name']
                    ,amount=int(child_row['amount']),communication=child_row['communication']
                    ,description=child_row['description'],deadline=child_row['deadline']
                    ,late_fee_category=child_row['late_fee_category'],deadline_date=child_row['deadline_date']
                    ,late_fee_type=child_row['late_fee_type'],late_fee_grace=child_row['late_fee_grace']
                    ,late_fee_date=child_row['late_fee_date'],late_fee_max=child_row['late_fee_max']
                    ,late_fee_amount=child_row['late_fee_amount'],created_on=created_on,added_by=self.request.user
                    )
                instance.amount=total_amount
                instance.save()
                email_data=[]
                email=row.tenant.email
                type_id=instance.id
                invoice_id=instance.statement_invoice
                subject="Invoice"
                if communication=='email':
                    lease_id = urlsafe_base64_encode(smart_bytes(lease_title))
                    invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
                    relativeLink = reverse(
                                'tenant_dashboard:invoice-pdf', kwargs={'lease': lease_id,'statement':statement,'invoice': invoice_id})
                    current_site =  request.META['HTTP_HOST']
                    # relativeLink = reverse('property:dashboard')
                    absurl =settings.SITE_PROTOCOL+current_site+relativeLink
                    success=0
                    fail=0
                    if email:
                        status='sent'
                        reason=None
                        property_name=row.unit.unit_property.property_name
                        lease_info=f'{row.unit.unit_name} {property_name}'
                        body=f'Hope you are well. You are getting this invoice because you are a tenant of {lease_info}'
                        template='email_templates/finance.html'
                        email_data.append({'subject':"Invoice", 'to':email,'from':request.user.email,
                                'name':row.tenant.name,'property':property_name,'body':body,'color':'#4b72fa','template':template,'amount':total_amount,'document':None,'href':absurl })
                        Util.send_email(email_data)
                        success+=1
                    else:
                        status='not sent'
                        reason='email not found'
                        fail+=1
                    Email.objects.create(
                    lease=lease
                   ,email_sent_to=email,body=body,subject=subject
                    ,group='finance',type='invoice',type_id=type_id,status=status,document=None
                    ,reason=reason,added_by=self.request.user
                    )
                    if fail==0:
                        success_insert='Invoices have been created and sent'
                    else:
                        success_insert=f'Invoices have been created however, {fail} emails were not sent due to lack of email address. '
                # serializer.save(added_by=self.request.user,tenant=row.tenant,unit=row.unit,property=row.unit.unit_property)


            # print(serializer.data)
            
            print('------------------------------------------------------')
            # print(final_data)

            # serializer.saved(added_by=self.request.user)

            # property_auto= serializer.data['id']
            # property_name= request.POST.get('property_name')
         
            return Response({
                
                # 'response': serializer.data,
                'success': success_insert,
            })
        else:
            error_response = error_loop.fix_errors_bulk(serializer.errors)
            print("serialiser errors",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        # print(self.request.user.user_type)
        # data=Invoice.objects.raw('''
    
        #  SELECT "finance_invoice"."invoice_group_id", COUNT("finance_invoice"."id") AS "ni" FROM "finance_invoice" GROUP BY "finance_invoice"."invoice_group_id"
        # ''')
        # data=Statement.objects.annotate(count_data=Count('invoice__invoice_group')).order_by().prefetch_related('invoice__invoice_group')
        # data=Invoice.objects.annotate(count_data=Count('amount')).order_by()
        # data=Invoice.objects.annotate(perm_count=Count('tenant'))
        # data=Statement.objects.annotate(perm_count=Count('invoice_statements')).prefetch_related('invoice_statements__unit')


        # subquery_invoice = Statement.objects.filter(
        # id=OuterRef('id')
        # ).annotate(
        #     total_payment = Sum('amount')
        # ).values('total_payment')[:1]

        data=Invoice.objects.only('invoice_group','created_on','name','amount','lease__tenant__id','lease__unit__id','lease__tenant__name','lease__unit__unit_name','lease__unit__unit_property__property_name').select_related('invoice_group','lease__unit','lease__tenant','lease__unit__unit_property','lease')\
           .distinct('created_on','invoice_group').filter(invoice_type="invoice").order_by('-created_on','invoice_group_id')
        # data=Invoice.objects.only('invoice_group','created_on','name','amount','lease__tenant__id','lease__unit__id','lease__tenant__name','lease__unit__unit_name','lease__unit__unit_property__property_name').select_related('invoice_group','lease__unit','lease__tenant','lease__unit__unit_property','lease')\
        #    .distinct('invoice_group').filter(invoice_type="invoice")




        # data=[Invoice.objects.filter(amount=x['invoice_group'])
        # for x in Invoice.objects.values('invoice_group').annotate(perm_count=Count('invoice_group'))
        # ]
#         [ModelTest.objects.get(test_field=x['test_field'],test_date=x['td'])
#      for x in ModelTest.objects.values('test_field').annotate(td=Max('test_date'))
# ]
        # data = Invoice.objects.all().annotate(Count('invoice_group', 
        #                                  distinct=True))
        # data=Statement.objects.filter(type='invoice').select_related('id')
        # tesy=invoice.obje


# SELECT "finance_invoice"."invoice_group_id", COUNT("finance_invoice"."invoice_group_id") AS "invoice_group__count" FROM "finance_invoice" GROUP BY "finance_invoice"."invoice_group_id"
       
       
       
        # <QuerySet [<Invoice: Invoice object (12)>, <Invoice: Invoice object (15)>, <Invoice: Invoice object (10)>, <Invoice: Invoice object (13)>, <Invoice: Invoice object (9)>, <Invoice: Invoice object (8)>, <Invoice: Invoice object (11)>, <Invoice: Invoice object (14)>]>
        # <QuerySet [{'amount': 150, 'ni': 2}, {'amount': 250, 'ni': 2}, {'amount': 500, 'ni': 1}, {'amount': 2000, 'ni': 1}, {'amount': 7500, 'ni': 2}]>
        print('-----------------------------------------')
        print(data.query)
        for row in data:
            # print("id:",row.id)
            print("amount:",row)
        
        print('****************************************8')
        print(data)
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease__tenant__name','lease__unit__unit_name','invoice_group__statement_invoice')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            cancelled_message=''
           
            
            status=f'<span class="badge light badge-primary rounded">Partially paid</span>'
            view_payments=f'<a class="dropdown-item view_payments_button " id="{row.invoice_group.id}">View payments</a>'
           
            if  row.invoice_group.amount <=   row.invoice_group.amount_sorted:
                status=f'<span class="badge light badge-success rounded">Invoice paid</span>'
            if  row.invoice_group.amount_sorted <1:
                 status=f'<span class="badge light rounded badge-danger">Not paid</span>'
                 view_payments=""
            if  row.is_cancelled:
                cancelled_message=f'<br><small class="text-danger font-w600 fancy_text5">(Invoice was cancelled)</small>'
                view_payments=""
                status=f'<span class="badge light rounded badge-dark">Invoice was cancelled</span>'
            
            data.append ([
            #    row.ni,
                f''' {row.invoice_group.statement_invoice}
                {cancelled_message}
                ''',
                # row.invoice_group.amount,
                 '{:,}'.format(row.invoice_group.amount),
                
                status,
            #   status,
                 row.created_on.strftime("%d %b, %Y"),
                f'''   
                {row.lease.tenant.name}
                <br>
                   {row.lease.unit.unit_name}
         
                ''',
               f''' 
                <div class="dropdown float-right">
                    <button type="button"
                        class="btn btn-primary light sharp btn-rounded"
                        data-toggle="dropdown" aria-expanded="false">
                        <svg width="20px" height="20px" viewBox="0 0 24 24"
                            version="1.1">
                            <g stroke="none" stroke-width="1" fill="none"
                                fill-rule="evenodd">
                                <rect x="0" y="0" width="24" height="24"></rect>
                                <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                            </g>
                        </svg>
                    </button>
                    <div class="dropdown-menu" x-placement="bottom-start"
                        style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                       
                        <a class="dropdown-item edit_invoice_button text-primary" id="{row.invoice_group.id}">View</a>
                        {view_payments}
                         <hr>
                        <a class="dropdown-item" href="{reverse('finance:invoice-document', kwargs={'invoice': row.invoice_group.statement_invoice })}">Open the invoice</a>
                        <a class="dropdown-item" href="{reverse('finance:invoice-pdf', kwargs={'invoice': row.invoice_group.statement_invoice })}">Download the invoice</a>

                      

                    </div>
                </div>
               ''',
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

class ListCreate_creditnote(custom_apiviews.ListBulkCreateAPIView):


    data = []
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers
    success_insert='Your creditnote has been created'
  
    def create(self, request, format=None, *args, **kwargs):
        success_insert=self.success_insert
        select_invoice=request.POST.get('select_invoice')
        statement=str(uuid.uuid4()).replace("-","").upper()
        statement_invoice = select_invoice.split(',')[0]
        lease = select_invoice.split(',')[2]
        print("))))))))))))))))))))")
        print(select_invoice)
        invoice_group_bulk=generate_transaction_id()
        
        created_on=datetime.datetime.now()
        query=Statement.objects.get(statement_invoice=statement_invoice)
        invoice=Invoice.objects.filter(invoice_group=query.id)
        invoice_group=f'CRED{lease}{invoice_group_bulk}'
        print("grrrrrrrrrrrrroup",invoice_group)
        instance=Statement.objects.create(statement_invoice=invoice_group,lease=query.lease,type='credit note',amount=-query.amount,created_on=created_on,added_by=self.request.user)
        ids=[]
        for row in invoice:
            Invoice.objects.create(added_on=row.added_on
            ,lease=row.lease,invoice_type="credit note"
            ,invoice_group=instance,invoice_group_bulk=invoice_group_bulk
            ,name=row.name,cancelled_invoice=invoice[0]
            ,amount=-row.amount,communication=row.communication
            ,description=row.description,deadline=row.deadline
            ,late_fee_category=row.late_fee_category,deadline_date=row.deadline_date
            ,late_fee_type=row.late_fee_type,late_fee_grace=row.late_fee_grace
            ,late_fee_date=row.late_fee_date,late_fee_max=row.late_fee_max
            ,late_fee_amount=row.late_fee_amount,created_on=created_on,added_by=self.request.user
            )
            ids.append(row.id)

        Receipt.objects.filter(invoice__in=list(ids)).update(invoice=None,is_prepayment=True)
        query.amount_sorted=0
        query.save()
        invoice.update(is_cancelled=True)

        email_data=[]
        email=query.lease.tenant.email
        lease_title=query.lease.id
        lease=query.lease
        # type_id=query.id
        # invoice_id=query.statement_invoice
        type_id=instance.id
        invoice_id=invoice_group
        subject="Credit note"
        
        
        lease_id = urlsafe_base64_encode(smart_bytes(lease_title))
        invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
        
        relativeLink = reverse(
                    'tenant_dashboard:invoice-pdf', kwargs={'lease': lease_id,'statement':statement,'invoice': invoice_id})
        current_site =  request.META['HTTP_HOST']
        # relativeLink = reverse('property:dashboard')
        absurl =settings.SITE_PROTOCOL+current_site+relativeLink
        success=0
        fail=0
        if email:
            status='sent'
            reason=None
            property_name= query.lease.unit.unit_property.property_name
            lease_info=f'{query.lease.unit.unit_name} {property_name}'
            body=f'Hope you are well. You are getting this credit note because you are a tenant of {lease_info} and an invoice was cancelled'
            template='email_templates/finance.html'
            email_data.append({'subject':"Credit note(cancelled invoice)", 'to':email,'from':request.user.email,
                    'name':query.lease.tenant.name,'property':property_name,'body':body,'color':'#D98880','template':template,'amount':-query.amount,'document':None,'href':absurl })
        
            Util.send_email(email_data)
            success+=1
        else:
            status='not sent'
            reason='email not found'
            fail+=1
        Email.objects.create(
        lease=lease
        ,email_sent_to=email,body=body,subject=subject
        ,group='finance',type='credit note',type_id=type_id,status=status,document=None
        ,reason=reason,added_by=self.request.user
        
        )
        if fail==0:
            success_insert='Credit note has been created and sent'
        else:
            success_insert=f'Credit note has been created however, {fail} emails were not sent due to lack of email address. '

        
        return Response({
                
                # 'response': serializer.data,
                'success': success_insert,
            })
       

    def get_queryset(self):
        data=Invoice.objects.only('invoice_group','created_on','name','amount','lease__tenant__id','lease__unit__id','lease__tenant__name','lease__unit__unit_name','lease__unit__unit_property__property_name').select_related('invoice_group','lease__unit','lease__tenant','lease__unit__unit_property','lease')\
             .distinct('created_on','invoice_group').filter(invoice_type="credit note").order_by('-created_on','invoice_group_id')

 
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease__tenant__name','lease__unit__unit_name','invoice_group__statement_invoice')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            
       
            data.append ([
            #    row.ni,
                row.invoice_group.statement_invoice,
                # row.invoice_group.amount,
                row.invoice_group.amount,
            
                 row.created_on.strftime("%d %b, %Y"),
                f'''   
                {row.lease.tenant.name}
                <br>
                   {row.lease.unit.unit_name}

                  
                ''',
               f''' 
                <div class="dropdown float-right">
                    <button type="button"
                        class="btn btn-danger light sharp btn-rounded"
                        data-toggle="dropdown" aria-expanded="false">
                        <svg width="20px" height="20px" viewBox="0 0 24 24"
                            version="1.1">
                            <g stroke="none" stroke-width="1" fill="none"
                                fill-rule="evenodd">
                                <rect x="0" y="0" width="24" height="24"></rect>
                                <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                            </g>
                        </svg>
                    </button>
                    <div class="dropdown-menu" x-placement="bottom-start"
                        style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                        <a class="dropdown-item" href="{reverse('finance:invoice-document', kwargs={'invoice': row.invoice_group.statement_invoice })}">Open the credit note</a>
                        <a class="dropdown-item" href="{reverse('finance:invoice-pdf', kwargs={'invoice': row.invoice_group.statement_invoice })}">Download the credit note</a>


                      

                    </div>
                </div>
               ''',
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

class ListCreate_debitnote(custom_apiviews.ListBulkCreateAPIView):


    data = []
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers
    success_insert='The receipt has been cancelled'
  
    def create(self, request, format=None, *args, **kwargs):
        select_payment=request.POST.get('select_payment')
        statement_receipt = select_payment.split(',')[0]
        lease = select_payment.split(',')[2]
        success_insert=self.success_insert
        receipt_group_bulk=generate_transaction_id()
        
        created_on=datetime.datetime.now()
        query=Statement.objects.get(statement_receipt=statement_receipt)
        receipt=Receipt.objects.filter(receipt_group=query.id)
        receipt_group=f'DEB{lease}{receipt_group_bulk}'
        print("grrrrrrrrrrrrroup",receipt_group)
        instance=Statement.objects.create(statement_receipt=receipt_group,lease=query.lease,type='debit note',amount=-query.amount,created_on=created_on,added_by=self.request.user)
        ids=[]
        invoice_groups=[]
        has_invoice=False



        for row in receipt:
            Receipt.objects.create(added_on=row.added_on
            ,lease=row.lease,receipt_type="debit note",cancelled_receipt=receipt[0]
            ,receipt_group=instance,is_prepayment=row.is_prepayment
            ,amount=-row.amount,communication=row.communication
            ,description=row.description,invoice=row.invoice
            ,ref_no=row.ref_no,paid_through=row.paid_through
            ,created_on=created_on,created_time=row.created_time,added_by=self.request.user
            
            )
            print("++++++++++++++++++")
            print(row.invoice)
            if row.invoice:
                ids.append(row.invoice.id)
                invoice_groups.append(row.invoice.invoice_group.id)
                has_invoice=True

           
        if has_invoice:
            invoice=Invoice.objects.filter(id__in=list(ids))
            invoice.update(amount_sorted=0)
            print("====================================")
            print(invoice_groups)
            statement=Statement.objects.filter(id__in=list(invoice_groups))
            statement.update(amount_sorted=0)
       
        receipt.update(is_cancelled=True)
        
        email_data=[]
        email=query.lease.tenant.email
        lease_title=query.lease.id
        lease=query.lease
        # type_id=query.id
        # invoice_id=query.statement_invoice
        type_id=instance.id
        invoice_id=receipt_group
        subject="Debit note"
        
        statement=str(uuid.uuid4()).replace("-","").upper()
        lease_id = urlsafe_base64_encode(smart_bytes(lease_title))
        invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
        
        relativeLink = reverse(
                    'tenant_dashboard:receipt-pdf', kwargs={'lease': lease_id,'statement':statement,'receipt': invoice_id})
        current_site =  request.META['HTTP_HOST']
        # relativeLink = reverse('property:dashboard')
        absurl =settings.SITE_PROTOCOL+current_site+relativeLink
        success=0
        fail=0
        if email:
           
            status='sent'
            reason=None
            property_name= query.lease.unit.unit_property.property_name
            lease_info=f'{query.lease.unit.unit_name} {property_name}'
            body=f'Hope you are well. You are getting this debit note because you are a tenant of {lease_info} and a payment was cancelled'
            template='email_templates/finance.html'
            email_data.append({'subject':"Debit note(cancelled receipt)", 'to':email,'from':request.user.email,
                    'name':query.lease.tenant.name,'property':property_name,'body':body,'color':'#D98880','template':template,'amount':-query.amount,'document':None,'href':absurl })
        
            Util.send_email(email_data)
            success+=1
        else:
            status='not sent'
            reason='email not found'
            fail+=1
        Email.objects.create(
        lease=lease
        ,email_sent_to=email,body=body,subject=subject
        ,group='finance',type='debit note',type_id=type_id,status=status,document=None
        ,reason=reason,added_by=self.request.user
        
        )
        if fail==0:
            success_insert='Debit note has been created and sent'
        else:
            success_insert=f'Debit note has been created however, {fail} emails were not sent due to lack of email address. '

        return Response({
                
                # 'response': serializer.data,
                'success': success_insert,
            })
       

    def get_queryset(self):
            data=Receipt.objects.only('receipt_group','created_on','amount','lease__tenant__id','lease__unit__id','lease__tenant__name','lease__unit__unit_name','lease__unit__unit_property__property_name').select_related('receipt_group','lease__unit','lease__tenant','lease__unit__unit_property','lease')\
                .distinct('created_on','receipt_group').filter(receipt_type="debit note").order_by('-created_on','receipt_group_id')
            return data

    def filter_for_datatable(self, queryset):

        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease__tenant__name','lease__unit__unit_name','amount','receipt_group__statement_receipt')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
    
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            
            status=f'<span class="badge light badge-success rounded">Completer</span>'
        
            if  row.receipt_group.amount >   row.receipt_group.amount_sorted:
                    status=f'<span class="badge light rounded badge-danger">Not complete</span>'
    
            
            data.append ([
            #    row.ni,
                row.receipt_group.statement_receipt,
                # row.invoice_group.amount,
                
                row.receipt_group.amount,
                row.paid_through,
                row.created_on.strftime("%d %b, %Y"),
                f'''   
                {row.lease.tenant.name}
                <br>
                {row.lease.unit.unit_name}
         
                ''',
            f''' 
                <div class="dropdown float-right">
                    <button type="button"
                        class="btn btn-primary light sharp btn-rounded"
                        data-toggle="dropdown" aria-expanded="false">
                        <svg width="20px" height="20px" viewBox="0 0 24 24"
                            version="1.1">
                            <g stroke="none" stroke-width="1" fill="none"
                                fill-rule="evenodd">
                                <rect x="0" y="0" width="24" height="24"></rect>
                                <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                            </g>
                        </svg>
                    </button>
                    <div class="dropdown-menu" x-placement="bottom-start"
                        style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                        <a class="dropdown-item edit_receipt_button text-primary" id="{row.receipt_group.id}">View</a>
                        <hr>
                        <a class="dropdown-item" href="{reverse('finance:receipt-document', kwargs={'receipt': row.receipt_group.statement_receipt })}">Open the debit note</a>
                        <a class="dropdown-item" href="{reverse('finance:receipt-pdf', kwargs={'receipt': row.receipt_group.statement_receipt })}">Download the debit note</a>

                    </div>
                </div>
            ''',
            
            
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def invoice_details(request,*args, **kwargs):
    invoice=request.GET.get('invoice')
    print("------------------------------------****(((999 777 999")
    print(invoice)
    
    invoices_query=Invoice.objects.filter(invoice_group=invoice).order_by('-created_on').select_related("invoice_group")

    data = []
    details_id="-------"
    details_amount="-------"
    details_created_on="-------"
    details_communication="-------"
    details_description=None
    
    for row in invoices_query:   
            details_id=row.invoice_group.statement_invoice
            details_id=row.invoice_group.statement_invoice
            details_amount=row.invoice_group.amount
            details_created_on=row.created_on.strftime("%d %b, %Y"),
            details_communication=row.communication
            if row.communication=="email":
                details_communication=f'{row.communication} with a digital invoice'
            details_description=row.description
                        
            status=f'<span class="badge light badge-primary rounded">Partially paid</span>'
           
            if  row.amount <=   row.amount_sorted:
                status=f'<span class="badge light badge-success rounded">Invoice paid</span>'
            if  row.amount_sorted <1:
                 status=f'<span class="badge light rounded badge-danger">Not paid</span>'
            data.append ([
    
            row.name,
            row.amount,
            row.amount_sorted,
            status,
            # row.late_fee,
            
    
              ])

       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
            'details_id': details_id,
            'details_amount': details_amount,
            'details_created_on': details_created_on,
            'details_communication': details_communication,
            'details_description': details_description,
    
         
        }
    return Response(response)
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def receipt_details(request,*args, **kwargs):
    receipt=request.GET.get('receipt')
    print("------------------------------------****(((999 777 999")
    print(receipt)
    
    receipts_query=Receipt.objects.filter(receipt_group=receipt).order_by('-created_on').select_related("receipt_group")


    details_id="-------"
    details_amount="-------"
    details_created_on="-------"
    details_communication="-------"
    details_ref="-------"
    details_paid_through="-------"
    details_description=None
    
    for row in receipts_query:   
            details_id=row.receipt_group.statement_receipt
        
            details_amount=row.receipt_group.amount
            details_created_on=row.created_on.strftime("%d %b, %Y"),
            details_communication=row.communication
            if row.communication=="email":
                details_communication=f'{row.communication} with a digital invoice'
            details_description=row.description
            details_ref=row.ref_no
            details_paid_through=row.paid_through
                        

       
    response = {
    
            'details_id': details_id,
            'details_amount': details_amount,
            'details_created_on': details_created_on,
            'details_communication': details_communication,
            'details_description': details_description,
            'details_ref': details_ref,
            'details_paid_through': details_paid_through,
    
         
        }
    return Response(response)

@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def payments_made(request,*args, **kwargs):
    invoice=request.GET.get('invoice')
    invoices_query = Invoice.objects.filter(invoice_group=invoice)
    ids = invoices_query.values_list('pk', flat=True)

    # list method get ids without parse the returning queryset

 
    
    query=Receipt.objects.filter(invoice__in=list(ids),is_cancelled=False,receipt_type="payment").select_related("receipt_group")
    data = []


    for row in query:   
  

            data.append ([
    
            row.receipt_group.statement_receipt,
            row.amount,
            row.paid_through,
            f'{row.created_on.strftime("%d %b, %Y")} ',
            # row.late_fee,
            
    
              ])

       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
          
         
        }
    return Response(response)


class EditDelete_payments(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class =ReceiptSerializers
    queryset = Receipt.objects.all()
    success_update='The payment was updated'
    success_delete='The payment was deleted'

    def get_queryset(self):
        return Receipt.objects.all()


    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}




class ListCreate_payments(custom_apiviews.ListBulkCreateAPIView):
    # SELECT "finance_invoice"."invoice_group_id", COUNT("finance_invoice"."invoice_group_id") AS "ni" FROM "finance_invoice" GROUP BY "finance_invoice"."invoice_group_id"
    data = []
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers
    success_insert='Your receipt has been added'

    def create(self, request, format=None, *args, **kwargs):
        success_insert=self.success_insert
        unit_list=request.POST.get('unit_list').split(",") 
        created_on=request.POST.get('created_on')
        created_time=request.POST.get('created_time')
        communication=request.POST.get('communication')
        statement=str(uuid.uuid4()).replace("-","").upper()
        unit_list=[int(i) for i in unit_list]
        request.data._mutable = True
        invoice_group_bulk=generate_transaction_id()
        look_at=3
       
        raw_data=bulk_data_fomart_receipt(request.data,look_at)
        many = isinstance(raw_data, list)
        serializer = self.get_serializer(data=raw_data, many=many)
        leases=Lease.objects.filter(id__in=unit_list)
    
        if serializer.is_valid():
            # print('------------------------------------------------------')
            data=serializer.data
            for row in leases:
                lease=row
                lease_title=row.id
                total_amount=0
                receipt_group=f'RCPT{lease_title}{invoice_group_bulk}'
                instance=Statement.objects.create(statement_receipt=receipt_group,lease=lease,type='payment',amount=total_amount,created_on=created_on,added_by=self.request.user)
                for child_row in data:
                    if child_row['amount'] >0:
                        child_row['lease']=lease
                        if child_row['is_prepayment']=='yes' or child_row['is_prepayment']==True:
                            child_row['is_prepayment']=True
                            child_row['invoice']=None
                        else:
                            child_row['is_prepayment']=False
                            invoice_data = Invoice.objects.get(id=child_row['solution_invoice'])
                            child_row['invoice']=invoice_data
                            if child_row['amount']>0:
                                invoice_data.amount_sorted = invoice_data.amount_sorted + child_row['amount']
                                invoice_data.save()
                                statement_data = Statement.objects.get(id=invoice_data.invoice_group.id)
                                statement_data.amount_sorted = statement_data.amount_sorted + child_row['amount']
                                statement_data.save()

                        total_amount+=child_row['amount']
                        Receipt.objects.create(added_on=child_row['added_on']
                        ,lease=child_row['lease']
                        ,receipt_group=instance,is_prepayment=child_row['is_prepayment']
                        ,amount=child_row['amount'],communication=child_row['communication']
                        ,description=child_row['description'],invoice=child_row['invoice']
                        ,ref_no=child_row['ref_no'],paid_through=child_row['paid_through']
                        ,created_on=created_on,created_time=created_time,added_by=self.request.user
                        
                        )
                instance.amount=total_amount
                instance.save()

                email_data=[]
                email=row.tenant.email
                type_id=instance.id
                invoice_id=instance.statement_receipt
                subject="Receipt"
                
                if communication=='email':
                    lease_id = urlsafe_base64_encode(smart_bytes(lease_title))
                    invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
                    
                    relativeLink = reverse(
                                'tenant_dashboard:receipt-pdf', kwargs={'lease': lease_id,'statement':statement,'receipt': invoice_id})
                    current_site =  request.META['HTTP_HOST']
                    # relativeLink = reverse('property:dashboard')
                    absurl =settings.SITE_PROTOCOL+current_site+relativeLink
                    success=0
                    fail=0
                    if email:
                        status='sent'
                        reason=None
                        property_name=row.unit.unit_property.property_name
                        lease_info=f'{row.unit.unit_name} {property_name}'
                        body=f'Hope you are well. You are getting this receipt because you are a tenant of {lease_info}.'
                        template='email_templates/finance.html'
                        email_data.append({'subject':"Receipt", 'to':email,'from':request.user.email,
                                'name':row.tenant.name,'property':property_name,'body':body,'color':'#7DCEA0','template':template,'amount':total_amount,'document':None,'href':absurl })
                    
                        Util.send_email(email_data)
                        success+=1
                    else:
                        status='not sent'
                        reason='email not found'
                        fail+=1
                    Email.objects.create(
                    lease=lease
                    ,email_sent_to=email,body=body,subject=subject
                    ,group='finance',type='receipt',type_id=type_id,status=status,document=None
                    ,reason=reason,added_by=self.request.user
                    )
                    if fail==0:
                        success_insert='The receipt has been created and emailed'
                    else:
                        success_insert=f'The receipts has been created however, the email has not been sent due to lack of email address. '


         
            return Response({
                'success': success_insert,
            })
        else:
            error_response = error_loop.fix_errors_bulk(serializer.errors)
            print("serialiser errors",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        prepayment = Receipt.objects.filter(
        receipt_group=OuterRef('receipt_group'),is_prepayment=True
        ).annotate(
            total_payment = Sum('amount')
        ).values('total_payment')[:1]

        
        data=Receipt.objects.annotate(total_prepayment=Subquery(prepayment)).only('receipt_group','created_on','amount','lease__id','lease__tenant__id','lease__unit__id','lease__tenant__name','lease__unit__unit_name','lease__unit__unit_property__property_name').select_related('receipt_group','lease__unit','lease__tenant','lease__unit__unit_property','lease')\
            .distinct('created_on','receipt_group').filter(receipt_type="payment").order_by('-created_on','receipt_group_id')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease__tenant__name','lease__unit__unit_name','amount','receipt_group__statement_receipt')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            prepayment_button=''
            prepayment_message=''
            if row.total_prepayment:
                prepayment_button=f'<a class="dropdown-item prepayment_button text-primary" id="{row.id},{row.lease.id},{row.total_prepayment}">Match to an invoice</a>'
                prepayment_message=f'<br><div class="text-primary fs-14 fancy_text4">Prepayment of ({row.total_prepayment})</div>'
            cancelled_message=''
           
            if  row.is_cancelled:
                cancelled_message=f'<br><small class="text-danger font-w600 fancy_text5">(Receipt was cancelled)</small>'
                prepayment_button=''
         
    
            
            data.append ([
            #    row.ni,
               f''' {row.receipt_group.statement_receipt}
              
               {cancelled_message}
               {prepayment_message}
               
               '''
               ,
                # row.invoice_group.amount,
                  '{:,}'.format(row.receipt_group.amount),
            
                row.paid_through,
                 row.created_on.strftime("%d %b, %Y"),
                f'''   
                {row.lease.tenant.name}
                <br>
                   {row.lease.unit.unit_name}
         
                ''',
               f''' 
                <div class="dropdown float-right">
                    <button type="button"
                        class="btn btn-primary light sharp btn-rounded"
                        data-toggle="dropdown" aria-expanded="false">
                        <svg width="20px" height="20px" viewBox="0 0 24 24"
                            version="1.1">
                            <g stroke="none" stroke-width="1" fill="none"
                                fill-rule="evenodd">
                                <rect x="0" y="0" width="24" height="24"></rect>
                                <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                                <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                            </g>
                        </svg>
                    </button>
                    <div class="dropdown-menu" x-placement="bottom-start"
                        style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                        <a class="dropdown-item edit_receipt_button text-primary" id="{row.receipt_group.id}">View</a>
                        {prepayment_button}
                         <hr>
                        <a class="dropdown-item" href="{reverse('finance:receipt-document', kwargs={'receipt': row.receipt_group.statement_receipt })}">Open the receipt</a>
                        <a class="dropdown-item" href="{reverse('finance:receipt-pdf', kwargs={'receipt': row.receipt_group.statement_receipt })}">Download the receipt</a>
                    </div>
                </div>
               ''',
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)



class EditDelete_payee(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The payee was updated successfully'
    success_delete='The payee was deleted successfully'
    serializer_class = PayeeSerializers
    queryset = Payee.objects.all()
    def get_queryset(self):
        return Payee.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_payee(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializers
    success_insert='The payee has been added'
    def get_queryset(self):
     
        # data = Payee.objects.all().prefetch_related('expenses')
        data =Payee.objects.annotate(amount=Sum(Subquery(
            Expense.objects.filter(payee=OuterRef('id')).values('payee__id').annotate(total_amount=Sum('amount')).values('total_amount')[:1]
         )))
         
        # data =Payee.objects.annotate(amount=Subquery(
        #     Expense.objects.filter(payee=OuterRef('id')).values('amount')[:1]
        #  ))
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'payee_category')
            ).filter(search__icontains=search_query)
        return queryset
    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            company=''
            if row.company_name:
                company=f"<br>({row.company_name})"
            data.append([
                   f'''          
            {row.name}{company}
                  ''',
                row.payee_category,
                row.amount,
                  f'''
                <div class="dropdown float-right">
                <button type="button"
                    class="btn btn-primary light sharp btn-rounded"
                    data-toggle="dropdown" aria-expanded="false">
                    <svg width="20px" height="20px" viewBox="0 0 24 24"
                        version="1.1">
                        <g stroke="none" stroke-width="1" fill="none"
                            fill-rule="evenodd">
                            <rect x="0" y="0" width="24" height="24"></rect>
                            <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                        </g>
                    </svg>
                </button>
                <div class="dropdown-menu" x-placement="bottom-start"
                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">                                                      
                    <a class="dropdown-item edit_payee text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_payee text-primary" id="{row.id},{row.name}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)



class EditDelete_payment_option(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The payment option was updated successfully'
    success_delete='The payment option was deleted successfully'
    serializer_class = PaymentOptionsSerializers
    queryset = Payment_options.objects.all()
    def get_queryset(self):
        return Payment_options.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_payment_option(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Payment_options.objects.all()
    serializer_class = PaymentOptionsSerializers
    success_insert='The payment option has been added'
    def get_queryset(self):
     
        # data = Payee.objects.all().prefetch_related('expenses')
        data =Payment_options.objects.all().select_related('property').order_by('property__property_name')
         
        # data =Payee.objects.annotate(amount=Subquery(
        #     Expense.objects.filter(payee=OuterRef('id')).values('amount')[:1]
        #  ))
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'property__property_name', 'type')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            if row.name:
                payment_name=row.name
            else:
                payment_name="----------"
            if row.account_info:
                account_info=row.account_info
            else:
                account_info="--------"

          
            data.append([
               row.property.property_name,
                row.type,
                payment_name,
                account_info,
                  f'''
                <div class="dropdown float-right">
                <button type="button"
                    class="btn btn-primary light sharp btn-rounded"
                    data-toggle="dropdown" aria-expanded="false">
                    <svg width="20px" height="20px" viewBox="0 0 24 24"
                        version="1.1">
                        <g stroke="none" stroke-width="1" fill="none"
                            fill-rule="evenodd">
                            <rect x="0" y="0" width="24" height="24"></rect>
                            <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                        </g>
                    </svg>
                </button>
                <div class="dropdown-menu" x-placement="bottom-start"
                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">                                                      
                    <a class="dropdown-item edit_payment_option text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_payment_option text-primary" id="{row.id},{row.type}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)


class EditDelete_expense(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The expense was updated successfully'
    success_delete='The expense was deleted successfully'
    serializer_class = ExpenseSerializers
    queryset = Expense.objects.all()
    def get_queryset(self):
        return Expense.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_expense(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializers
    success_insert='The expense has been added'
    def create(self, request, format=None, *args, **kwargs):
        created_for=request.POST.get('created_for')
        request.data._mutable = True
        if created_for=='building':
            request.data['unit']=None
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            serializer.save(added_by=self.request.user)         
            return Response({
                'response': serializer.data,
               
                'success': self.success_insert,
                'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
     
        data = Expense.objects.all().order_by("property")
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'expense_name', 'amount')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        for row in row_data:
            if row.status=="paid":
                status="<span class='fancy_text5 text-success fs-16'>Paid </span>"
                payment=f'<hr><a class="dropdown-item add_payment text-primary mt-2" id="{row.id},edit" >View payment</a>'
                document=f'<a class="dropdown-item mb-2" href="{row.receipt.url}"  download>View receipt</a><hr>'
                amount=row.amount
            else:
                status="<span class='fancy_text5 text-danger fs-16'>Not paid </span>"
                payment=f'<a class="dropdown-item add_payment text-primary" id="{row.id},add" >Add payment</a>'
                document=''
                amount="-------"
            data.append([
                row.property.property_name,
                row.expense_name,
                amount,
               
                row.created_on.strftime("%d %b, %Y"),
                status,
                  f'''
                <div class="dropdown float-right">
                <button type="button"
                    class="btn btn-primary light sharp btn-rounded"
                    data-toggle="dropdown" aria-expanded="false">
                    <svg width="20px" height="20px" viewBox="0 0 24 24"
                        version="1.1">
                        <g stroke="none" stroke-width="1" fill="none"
                            fill-rule="evenodd">
                            <rect x="0" y="0" width="24" height="24"></rect>
                            <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                            <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                        </g>
                    </svg>
                </button>
                <div class="dropdown-menu" x-placement="bottom-start"
                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">                                                      
                    <a class="dropdown-item edit_expense text-primary" id="{row.id}" >View expense</a>
                    {payment}
                    {document}
                    <a class="dropdown-item remove_expense text-primary" id="{row.id},{row.expense_name}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)
    
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def unapplied_invoices(request,*args, **kwargs):
    select_amount=request.POST.get('select_amount')
    # amount=int(select_amount)
    lease=request.POST.get('select_lease')
    paid_through=request.POST.get('select_paid_through')
    invoices_query=Invoice.objects.filter(lease__id=lease,invoice_type="invoice",is_cancelled=False).order_by('created_on')
# ,invoice_type="invoice"
    data = []
    balance=int(select_amount)
    total_balance=0
    for row in invoices_query:
      
        if row.amount_sorted < row.amount:
            unapplied_amount=row.amount-row.amount_sorted
        # print("start amount:",amount,"start balance:",balance)
            if balance >=unapplied_amount:
                amount=unapplied_amount
                balance-=unapplied_amount
            elif balance<unapplied_amount and balance>0:
                amount=balance
                balance=0
            else:
                amount=0
                balance=0
            total_balance+=unapplied_amount
            new_amount=amount+row.amount_sorted
            print("end amount:",amount,"end balance:",balance)

        
            # if amount >0:
            #     amount=-unapplied_amount
            # else:
            #     amount=0

            

                    
            data.append ([
            
    
            f'{row.name} <small class="fancy_text5"><br>{row.amount}</small>',
            unapplied_amount,
            
            f'''{amount}
            <br>
            
            <input type="hidden" name="solution_invoice" value="{row.id}">
            <input type="hidden" name="is_prepayment" value="no">
            <input type="hidden" name="invoice_group" value="{row.invoice_group.id}">
            <input type="hidden" name="amount" value="{amount}">
            ''',
                
            ])
    if balance>0:
        data.append ([

        f'''<div class=" font-w600">prepayment</div>
        <small>{balance} will be marked as future payments<small>
        ''',
        0,
    
        f'''{balance}
        <br>
        
        <input type="hidden" name="solution_invoice" value="0">
        <input type="hidden" name="is_prepayment" value="yes">
        <input type="hidden" name="invoice_group" value="{None}">
        <input type="hidden" name="amount" value="{balance}">
        ''',
            
        ])

       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
            'amount': select_amount,
            'paid_through': paid_through,
            'total_balance': total_balance,
            'lease': lease,
         
        }
    return Response(response)
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def match_invoice(request,*args, **kwargs):
    select_amount=request.POST.get('amount')
    # amount=int(select_amount)
    lease=request.POST.get('lease')
    receipt_id=request.POST.get('receipt')
    print("-----------------------------------")
    print("amount:",select_amount,"amount:",lease,"amount:",receipt_id)
    invoices_query=Invoice.objects.filter(lease__id=lease,invoice_type="invoice",is_cancelled=False).order_by('created_on')
# ,invoice_type="invoice"
    has_invoice="No"
    if invoices_query:
        has_invoice="Yes"

    data = []
    balance=int(select_amount)
    total_balance=0
    
    for row in invoices_query:
      
        if row.amount_sorted < row.amount:
            unapplied_amount=row.amount-row.amount_sorted
        # print("start amount:",amount,"start balance:",balance)
            if balance >=unapplied_amount:
                amount=unapplied_amount
                balance-=unapplied_amount
            elif balance<unapplied_amount and balance>0:
                amount=balance
                balance=0
            else:
                amount=0
                balance=0
            total_balance+=unapplied_amount
            
            print("end amount:",amount,"end balance:",balance)

                    
            data.append ([
            
    
            f'{row.name} <small class="fancy_text5"><br>{row.amount}</small>',
            unapplied_amount,
            
            f'''{amount}
            <br>
            
            <input type="hidden" name="solution_invoice" value="{row.id}">
            <input type="hidden" name="is_prepayment" value="no">
            <input type="hidden" name="invoice_group" value="{row.invoice_group.id}">
            <input type="hidden" name="amount" value="{amount}">
            ''',
                
            ])
    if balance>0:
        data.append ([

        f'''<div class=" font-w600">prepayment</div>
        <small>{balance} will be marked as future payments<small>
        ''',
        0,
    
        f'''{balance}
        <br>
        
        <input type="hidden" name="solution_invoice" value="0">
        <input type="hidden" name="is_prepayment" value="yes">
        <input type="hidden" name="invoice_group" value="{None}">
        <input type="hidden" name="amount" value="{balance}">
        ''',
            
        ])

       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
            'amount': select_amount,
            'receipt_id': receipt_id,
            'total_balance': total_balance,
            'has_invoice': has_invoice,
            'lease': lease,
         
        }
    return Response(response)
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def submit_prepayment(request,*args, **kwargs):
    receipt_id=request.POST.get('receipt_id')
    look_at=0
    data=bulk_data_fomart_receipt(request.data,look_at)
    
    receipt=Receipt.objects.get(id=receipt_id)
    total_amount=0
    print(receipt)
   
    for child_row in data:
      
        # child_row['is_prepayment']=False
        # invoice_data = Invoice.objects.get(id= int(child_row['solution_invoice']))
        # child_row['invoice']=invoice_data

        if child_row['is_prepayment']=='yes' or child_row['is_prepayment']==True:
                    child_row['is_prepayment']=True
                    child_row['invoice']=None
        else:
            child_row['is_prepayment']=False
            invoice_data = Invoice.objects.get(id=child_row['solution_invoice'])
            child_row['invoice']=invoice_data
            if int(child_row['amount'])>0:
                invoice_data.amount_sorted = invoice_data.amount_sorted + int(child_row['amount'])
                invoice_data.save()
                statement_data = Statement.objects.get(id=invoice_data.invoice_group.id)
                statement_data.amount_sorted = statement_data.amount_sorted + int(child_row['amount'])
                statement_data.save()
       

        total_amount+= int(child_row['amount'])
        Receipt.objects.create(added_on=receipt.added_on
        ,lease=receipt.lease
        ,receipt_group=receipt.receipt_group,is_prepayment=child_row['is_prepayment']
        ,amount= int(child_row['amount']),communication=receipt.communication
        ,description=receipt.description,invoice=child_row['invoice']
        ,ref_no=receipt.ref_no,paid_through=receipt.paid_through
        ,created_on=receipt.created_on,created_time=receipt.created_time,added_by=receipt.added_by

        )
   
    receipt.delete()
    response = {
            'success': 'Successfully mapped your receipt',
         
        }
    return Response(response)

 
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def finance_history(request,*args, **kwargs):
    id=request.GET.get('id')
    type=request.GET.get('type')
    print("tyyyyyyyyyyyyyupe",type)

    if type=="tenant":
        query=Statement.objects.filter(lease__tenant=id).order_by("created_on")
    if type=="unit":
        query=Statement.objects.filter(lease__unit=id).order_by("created_on")
    if type=="property":
        if id !='all':
            query=Statement.objects.filter(lease__unit__unit_property=id).order_by("created_on")
        else:
            query=Statement.objects.all().order_by("created_on")
    


    data = []
    running_balance=0
    for row in query:
        debit="-----"
        credit="----"
        if row.type=="invoice" or row.type=="debit note":
            debit=row.amount
            if row.type=="debit note":
                debit=debit*-1
            # debit=row.amount
            running_balance+=debit
        else:
            credit=row.amount
            if row.type=="credit note":
                credit=credit*-1
            # credit=row.amount
            running_balance-=credit
        data.append ([
        row.created_on.strftime("%d %b, %Y"),
        row.type,
        debit,
        credit,
        running_balance
            
        ])
 
       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
            'running_balance': running_balance,
           
         
        }
    return Response(response)







class balances_table(custom_apiviews.ListBulkCreateAPIView):




    # SELECT "finance_invoice"."invoice_group_id", COUNT("finance_invoice"."invoice_group_id") AS "ni" FROM "finance_invoice" GROUP BY "finance_invoice"."invoice_group_id"

    data = []
    queryset = Receipt.objects.all()
   
        # Q(type='payment') | Q(type='debit note')
    def get_queryset(self):
        subquery_receipt = Statement.objects.filter(
        lease=OuterRef('lease')
        ).values('lease').annotate(
            total_payment = Sum('amount')
        ).filter(Q(type='payment') | Q(type='debit note')).values('total_payment')[:1]
        subquery_invoice = Statement.objects.filter(
        lease=OuterRef('lease')
        ).values('lease').annotate(
            total_invoice = Sum('amount')
        ).filter(Q(type='invoice') | Q(type='credit note')).values('total_invoice')[:1]
    

        data = Statement.objects.annotate(
            total_receipt=Subquery(subquery_receipt),
            total_invoice=Subquery(subquery_invoice),
           
        ).order_by().distinct('lease').select_related('lease__unit','lease__tenant','lease__unit__unit_property','lease')
        print("------------------------------------------------------------")
        print(data)




        
   
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease__tenant__name','lease__unit__unit_name')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
     
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        data = []
        row_data = filtered_queryset[start:end]
        record_total=0
        for row in row_data:
            invoice=row.total_invoice
            receipt=row.total_receipt
            if row.total_invoice is None:
                invoice=0
            if row.total_receipt is None:
                receipt=0
            
            balance=invoice-receipt
            if balance !=0:
                record_total+=1
                data.append ([

                f'''   
                    {row.lease.tenant.name}
                    <br>
                        {row.lease.unit.unit_name}
                  
                    ''',
            
                invoice,
                receipt,
                balance,
            
                
            
                    
                    ])
        response = {
            'draw': draw,
            'recordsTotal': record_total,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)


      




      
    
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def balances_table2(request,*args, **kwargs):
       
    subquery_invoice = Statement.objects.filter(
     lease=OuterRef('lease')
    ).values('lease').annotate(
        total_spent = Sum('amount')
    ).filter(type='invoice').values('total_spent')[:1]
    subquery_receipt = Statement.objects.filter(
     lease=OuterRef('lease')
    ).values('lease').annotate(
        total_spent = Sum('amount')
    ).filter(type='receipt').values('total_spent')[:1]

    query = Statement.objects.annotate(
        total_invoice=Subquery(subquery_invoice),
        total_receipt=Subquery(subquery_receipt)
    ).order_by().distinct('lease')

    # query=Statement.objects.all().select_related('lease__unit','lease__tenant','lease__unit__unit_property','lease')
    data = []

    for row in query:
        balance=row.total_invoice-row.total_receipt
        
        data.append ([

          f'''   
            {row.lease.tenant.name}
            <br>
                {row.lease.unit.unit_name}
         
            ''',
      
        row.total_invoice,
        row.total_receipt,
        balance,
       
        
     
            
            ])
 
       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,

         
        }
    return Response(response)

    
# Invoice.objects.only('name','amount','tenant','unit').filter()
# #all fields expept added_on

# Invoice.objects.defer('added_on').filter()
# #all fields expept added_on

def send_auto_invoice_emails(request):
    
    email_data=[]
    statement=str(uuid.uuid4()).replace("-","").upper()
    current_site=settings.SITE_URL
    protocol=settings.SITE_PROTOCOL
   
    data=Invoice.objects.filter(communication="sent2",created_by="system").select_related("invoice_group","lease","lease__unit","lease__tenant").distinct('invoice_group__id')
    for row in data:
        print("**********************************")
        print(row.lease.tenant.name," ---",row.name,"----",row.invoice_group.id)

        status='sent'


        # from_email=row.added_by.email
        # lease=row.lease
        # lease_id=row.lease.id
        # email=row.lease.tenant.email
        # name=row.lease.tenant.name
        # type_id=row.invoice_group.id
        # total_amount=row.invoice_group.amount
        # invoice_id=row.invoice_group.statement_invoice
        # subject="Invoice"

        # lease_id = urlsafe_base64_encode(smart_bytes(lease_id))
        # invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
        
        # relativeLink = reverse(
        #             'tenant_dashboard:invoice-pdf', kwargs={'lease': lease_id,'statement':statement,'invoice': invoice_id})
        # current_site =  current_site
        # absurl =settings.SITE_PROTOCOL+current_site+relativeLink
        # success=0
        # fail=0
        # if email:
        #     status='sent'
        #     reason=None
        #     property_name=row.lease.unit.unit_property.property_name
        #     lease_info=f'{row.lease.unit.unit_name} {property_name}'
        #     body=f'Hope you are well. You are getting this invoice because you are a tenant of {lease_info}'
        #     template='email_templates/finance.html'
        #     email_data.append({'subject':"Invoice", 'to':email,'from':from_email,
        #             'name':name,'property':property_name,'body':body,'color':'#4b72fa','template':template,'amount':total_amount,'document':None,'href':absurl })
        
        #     Util.send_email(email_data)
        #     success+=1
        # else:
        #     status='not sent'
        #     reason='email not found'
        #     fail+=1
        # Email.objects.create(
        # lease=lease
        # ,email_sent_to=email,body=body,subject=subject
        # ,group='finance',type='invoice',type_id=type_id,status=status,document=None
        # ,reason=reason,added_by=row.added_by
        
        # )
        invoice=Invoice.objects.filter(invoice_group=row.invoice_group)
        invoice.update(communication=status)
        # invoice=
        # tenant.update(occupancy_status="occupied")

    

def create_auto_invoice():
    
    unit_query=Unit.objects.filter(occupancy_status="occupied")
    today=datetime.date.today()
    day_once=today
    day_week=today.strftime("%A")
    day_month=today.day
    day_year=f'{today.day},{today.strftime("%B")}' 
    print("once_date:",day_once)
    print("day_week:",day_week)
    print("day_month:",day_month)
    print("day_year:",day_year)
    
    invoice_group_bulk=generate_transaction_id()
    
   
    for row in unit_query:
        
        if row.unit_charges:
            lease=Lease.objects.get(unit=row.id,active=True)
            finance_query=Charges.objects.filter(Q(id__in=row.unit_charges)).filter(Q(once_date=day_once,duration="once")|Q(week_date=day_week,duration="weekly")|Q(month_date=day_month,duration="monthly")|Q(year_date=day_year,duration="annually"))
            invoice_group=f'INV{lease.id}{invoice_group_bulk}'
            statement_done=0
            total_amount=0
            instance=None
            for r in finance_query:
                deadline='no'
                deadline_date=None
                notify="None"
                if statement_done==0:
                    instance=Statement.objects.create(statement_invoice=invoice_group,lease=lease,type='invoice',amount=0,created_on=today,added_by=row.added_by)
                total_amount+=r.amount
                if r.late_fee_amount > 0:
                    deadline_date = datetime.date.today() + datetime.timedelta(days=r.late_fee_grace)
                    deadline='yes'
                if r.notify=="email":
                    notify="to be sent"
                
                Invoice.objects.create(added_on=today
                ,lease=lease
                ,invoice_group=instance,invoice_group_bulk=invoice_group_bulk
                ,name=r.name
                ,amount=r.amount,communication=notify
                ,deadline=deadline
                ,late_fee_category=r.late_fee_category,deadline_date=deadline_date
                ,late_fee_type=r.late_fee_type,late_fee_grace=r.late_fee_grace
               ,late_fee_max=r.late_fee_max
                ,late_fee_amount=r.late_fee_amount,created_on=today,added_by=row.added_by,created_by="system"
                )
                statement_done=1
                print(lease.id, "  "  ,row.unit_name,"    ",r)
            if instance is not None:
                instance.amount=total_amount
                instance.save()
 
    return send_auto_invoice_emails()


def test(request):
    today=datetime.date.today()
    invoice=Invoice.objects.filter(is_cancelled=False,invoice_type="invoice",late_fee_amount__gt=0,deadline_date__lte=today,late_fee_status="active",amount_sorted__lt= F('amount')).exclude(late_fee_type__isnull=True)
    invoice_group_bulk=generate_transaction_id()
    for row in invoice:
        lease=row.lease
        invoice_group=f'INV{row.lease.id}{invoice_group_bulk}'
        amount_not_paid=row.amount-row.amount_sorted
        name=f"Late fee ({row.name})"
        overall_late_fee=0
        amount=0
        if row.late_fee_type=="one_time_fixed":
            late_fee_status="complete"
            amount=row.late_fee_amount
            overall_late_fee=amount
        if row.late_fee_type=="one_time_percent_unpaid":
            late_fee_status="complete"
            raw_amount=(row.late_fee_amount*amount_not_paid)/100
            amount=format(raw_amount, ".2f")     
            overall_late_fee=amount
        if row.late_fee_type=="one_time_percent_entire":
            late_fee_status="complete"
            raw_amount=(row.late_fee_amount*row.amount)/100
            amount=format(raw_amount, ".2f")  
            overall_late_fee=amount

        if row.late_fee_type=="daily_time_fixed":
            late_fee_status="active"
            amount=row.late_fee_amount
            overall_late_fee=amount+row.amount_late_fee
            if overall_late_fee >= row.late_fee_max:
                late_fee_status="complete"

        if row.late_fee_type=="daily_time_percent_unpaid": 
            late_fee_status="active"
            raw_amount=(row.late_fee_amount*amount_not_paid)/100
            amount=float(format(raw_amount, ".2f"))   
            overall_late_fee=float(format(raw_amount+row.amount_late_fee, ".2f"))   
            if overall_late_fee >= row.late_fee_max:
                late_fee_status="complete"  

        if row.late_fee_type=="daily_time_percent_entire":
            late_fee_status="active"
            raw_amount=(row.late_fee_amount*row.amount)/100
            amount=float(format(raw_amount, ".2f")) 
            print("rrrrrrraw amount",raw_amount) 
            overall_late_fee=float(format(raw_amount+row.amount_late_fee, ".2f"))   
            if overall_late_fee >= row.late_fee_max:
                late_fee_status="complete" 


        # deadline='no'
        # deadline_date=None
        # notify="to be sent"
        
        # instance=Statement.objects.create(statement_invoice=invoice_group,lease=lease,type='invoice',amount=amount,created_on=today,added_by=row.added_by)
     
 
        
        # Invoice.objects.create(added_on=today
        # ,lease=lease
        # ,invoice_group=instance,invoice_group_bulk=invoice_group_bulk
        # ,name=name
        # ,amount=amount,communication=notify
        # ,deadline=deadline
        # ,deadline_date=deadline_date
        # ,late_fee_type=None
        # ,created_on=today,added_by=row.added_by,created_by="system"
        # )
       
       
        # row.late_fee_status=late_fee_status
        # row.amount_late_fee=overall_late_fee
        # row.save()
      
        print("-----------------------------------------------------------------------------------------------------")
        print("lATE NAME name",row.late_fee_type,"Amount",row.late_fee_amount,"Deadline date:",row.deadline_date)


        print(row.id,"invoice name",row.name,"Amount charged",amount,"amount:",row.amount,"sorted:",row.amount_sorted,"new status",late_fee_status,"late fee amont",overall_late_fee)
        print("-----------------------------------------------------------------------------------------------------")
    

    
    
    
  
   
 
    # return send_auto_invoice_emails()
def test2(request):
    today=datetime.date.today()
    data_year= "26,February"
    data_year_day=data_year.split(',')[0]
    data_year_month=datetime.datetime.strptime(data_year.split(',')[1], "%B").month
    date_year_year=today.year

    date_month_day=9
    date_month_month=today.month
    date_month_year=today.year
    
    print("-----------------------------------")
    print("MONTH -- day:",date_month_day ,"Month:",date_month_month,"Year:",date_month_year)
    print("YEAR-----day:",data_year_day ,"Month:",data_year_month,"Year:",date_year_year)

    string_month_date = f"{date_month_day}/{date_month_month}/{date_month_year}"
    string_year_date = f"{data_year_day}/{data_year_month}/{date_year_year}"
    cooked_month_date = datetime.datetime.strptime(string_month_date, "%d/%m/%Y")
    cooked_year_date = datetime.datetime.strptime(string_year_date, "%d/%m/%Y")
   
    present = datetime.datetime.now()
    if cooked_month_date.date() < present.date():
        print("cooked month date is less")
    else:
        print("cooked month date is greter")
    print("----------------------------------------------")
    if cooked_year_date.date() < present.date():
        print("cooked year date is less")
    else:
        print("cooked year date is greter")
    

    # id_list=list(data)
    
    



    # expense=Expense.objects.filter(status="not paid")
    # for row in expense:
    #     print("naaame",row.expense_name,"staus",row.status)

    #     message=f"Attach payment document for {row.name} "
    #     title="Expense reminder"
    #     to_group="staff"
    #     to_id=None
    #     notification_type="expense"
    #     from_group="system"
    #     from_user=None
    #     foreign_instance=expense
    #     Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)






    # from datetime import datetime,timedelta
    # from notifications.models import Notification

    # query = Lease.objects.filter(end_lease_notice="sent",lease_type="fixed period",active=True,end_date__gte=datetime.today(),end_date__lte=datetime.today()+timedelta(days=45)).select_related("tenant","unit","unit__unit_property")
    # for row in query:
    #     message=f" The lease from {row.tenant.name} in {row.unit.unit_name}, {row.unit.unit_property.property_name} will expire in 45 days or less"
    #     title="Expiring lease"
    #     to_group="tenant"
    #     to_id=5
    #     notification_type="lease"
    #     from_group="system"
    #     from_user=None
    #     foreign_instance=row
    #     Notification.objects.create(lease=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)

    #     print(message)





        # print(f"{row.id}) {row.tenant.name} {row.unit.unit_name} {row.end_date}")
    # print("work copleted --------------------------")
    # test_celery.delay()

    
    # return HttpResponse("the is done")
    # query=Statem2ent.objects.prefetch_related('invoice_statements')
    # query=Statement.objects.all().values("created_on__month").annotate(total_amount=Sum("amount")).values("created_on","total_amount")
    # invoice='INV16503811A'
    # lease=1
    # # user = Tenant.objects.all()
    # # print(user.email)
    # lease = urlsafe_base64_encode(smart_bytes(lease))
    # invoice = urlsafe_base64_encode(smart_bytes(invoice))
    # relativeLink = reverse(
    #             'tenant_dashboard:invoice-pdf', kwargs={'lease': lease, 'invoice': invoice})
    # current_site =  request.META['HTTP_HOST']
    # # relativeLink = reverse('property:dashboard')
    # absurl =settings.SITE_PROTOCOL+current_site+relativeLink

    # print("-----------------------------------------------------")
    # print(absurl)
   

    # query=Statement.objects.get(statement_invoice=statement_invoice)
  
    # invoice=Invoice.objects.annotate(Sum('amount')).values("invoice_group__statement_invoice")



#     a_qs = A.objects.all().prefetch_related(
#     models.Prefetch('b_set',
   
#         queryset=B_queryset,
#         to_attr='b_records'
#     )
#    ) 
    # query=Statement.objects.first()
    # print(dir(query))
    # print("-------------------------------")
    # for row in query:
    #     print(row.type)
    # year=datetime.datetime.now().year
    # print("-------------------------------")
    # print(year)
    # subquery = Invoice.objects.filter(
    #  invoice_group=OuterRef('invoice_group')
    # ).values('invoice_group').annotate(
    #     total_spent = Sum('amount')
    # ).values('total_spent')[:1]

    # query = Invoice.objects.annotate(
    #     total_spent=Subquery(subquery)
    # ).order_by().distinct('invoice_group')




    # query=query.filter(type="payment")
    # print("-------------------------------")
    # months = {'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}
    
    # print(query.query)
    # for row in query:
    #     print("name",row.invoice_group,"amount",row.total_spent)
        
    # print("-------------------------------")
    # print(invoice.amount[0])


def test_reverse(self,*args, **kwargs):
    lease = smart_str(urlsafe_base64_decode(kwargs['lease']))
    invoice = smart_str(urlsafe_base64_decode(kwargs['invoice']))
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")
    print(f'lease: {lease} invoice: {invoice} ')