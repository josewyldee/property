from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from tenant.models import Lease,Tenant
from maintenance.models import Maintenance
from rest_framework.response import Response
from django.views.generic import TemplateView
from maintenance.models import Maintenance,Document
from django.contrib.postgres.search import SearchVector
from maintenance.serializers import MaintenanceSerializers,DocumentSerializers
from utils import custom_apiviews,error_loop,html_pdf
from django.http import HttpResponse
from finance.models import Invoice,Receipt,Payment_options
# import datetime
from datetime import datetime
# Create your views here.
from django.views.generic import View

from django.template.loader import get_template

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

class profile(TemplateView):
    
    
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            tenant=Tenant.objects.get(user=self.request.user.id)
            lease=Lease.objects.filter(tenant=tenant.id)
            print(tenant)
            if lease:
                context['lease'] =lease[0]
            context['tenant'] =tenant
            return context
    template_name = "tenant_dashboard/profile.html"


class index(TemplateView):
    template_name = "tenant_dashboard/index.html"




class maintenance(TemplateView):

    # def get(self, request):
    #     if self.request.user.is_tenant:
    #         return redirect('/tenant_dashboard/dashboard')

    #     return super(maintenance, self).get(request)

  

    template_name = "tenant_dashboard/index.html"
class dashboard(TemplateView):
    
    template_name = "tenant_dashboard/index.html"
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant=Tenant.objects.get(user=self.request.user.id)
        context['maintenance'] = Maintenance.objects.filter(tenant=tenant.id)
        lease=Lease.objects.filter(tenant=tenant.id)
        if lease:
            context['lease'] =lease[0]
        context['tenant'] =tenant
        return context



class EditDelete_maintenance(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The record was updated successfully'
    success_delete='The record was deleted successfully'
    serializer_class = MaintenanceSerializers
    queryset = Maintenance.objects.all()
    def get_queryset(self):
        return Maintenance.objects.all()



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        raw_data=request.POST.get('unit')
        tenant = raw_data.split(',')[0]
        unit = raw_data.split(',')[1]
        request.data._mutable = True
        request.data['tenant']=tenant
        request.data['unit']=unit
        # print("ddddddddddddddddddddddddddd")
        # print("request daaat",raw_data)
        # print(request.data)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': self.success_update,
                'response': serializer.data,
               
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_maintenance(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializers
    success_insert='The record has been added'
    def create(self, request, format=None, *args, **kwargs):
        raw_data=request.POST.get('unit')
        tenant = raw_data.split(',')[0]
        unit = raw_data.split(',')[1]
        request.data._mutable = True
        request.data['tenant']=tenant
        request.data['unit']=unit
        request.data['unit']=unit
        print("ddddddddddddddddddddddddddd")
        print("request daaat",raw_data)
        print(request.data)
       
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            saved_user2 = serializer.save(added_by=self.request.user)
            id= serializer.data['id']
            return Response({
                'id': id,
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
        data = Maintenance.objects.select_related('tenant','unit').filter(added_by=self.request.user.id).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'status')
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        row_data = self.filter_for_datatable(queryset)
        data = []
        time = datetime.now()
        for row in row_data:
            status=f'<span class="badge light badge-success">Complete</span>'
            if row.status=="in progress":
                status=f'<span class="badge light badge-primary">In progress</span>'
            if row.status=="not started":
                status=f'<span class="badge light badge-danger">Not started</span>'
            data.append([
                  f'''          
                    {row.tenant.name}<br>({row.unit.unit_name})<br>{row.category}
                  ''',
                  row.name,
                  f'''          
                   <span class="text-bold text-primary">Reported on: </span><br>({row.reported_on.strftime("%Y-%m-%d")})<br>({str(time.day - row.reported_on.day) + " days ago)"}
                  ''',
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
                    <a class="dropdown-item cost_button" id="{row.id}" >Open costs</a>
                    <a class="dropdown-item attach_photos" id="{row.id}" >Attach photos</a>
                    <a class="dropdown-item edit_maintenance" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_maintenance" id="{row.id},{row.name}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)

class EditDelete_document(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The photo was updated successfully'
    success_delete='The photo was deleted successfully'
    serializer_class = DocumentSerializers
    queryset = Document.objects.all()
    def get_queryset(self):
        return Document.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
class ListCreate_document(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Document.objects.all()
    serializer_class = DocumentSerializers
    success_insert='The photo has been added'
    def get_queryset(self):
        maintenance=self.request.query_params.get('maintenance')
        data = Document.objects.filter(maintenance=maintenance, added_by=self.request.user.id).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name',)
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        row_data = self.filter_for_datatable(queryset)
        data = []
        for row in row_data:
            data.append([
                 f'<img src="{row.document.url}" alt="unit photo" style="width:50px;height:50px;border:2px solid #D98880;">',
                row.name,
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
                    <a class="dropdown-item download_document" id="{row.id}" >Download</a>
                    <a class="dropdown-item remove_document" id="{row.id},{row.maintenance}" >Delete</a>
                </div>
            </div>''',
            
              
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)
   
class invoice_pdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template("finance/invoice_document.html")
        context = {}
        lease = smart_str(urlsafe_base64_decode(kwargs['lease']))
        invoice = smart_str(urlsafe_base64_decode(kwargs['invoice']))
        print("888888888888888888888888",invoice)
        invoice =Invoice.objects.filter(invoice_group__statement_invoice=invoice,lease=lease).order_by('-created_on').select_related("invoice_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')
        # print()
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
        lease = smart_str(urlsafe_base64_decode(kwargs['lease']))
        receipt = smart_str(urlsafe_base64_decode(kwargs['receipt']))
        receipt =Receipt.objects.filter(receipt_group__statement_receipt=receipt,lease=lease).order_by('-created_on').select_related("receipt_group","lease","lease__unit","lease__tenant",'lease__unit__unit_property','added_by')[:1]
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
