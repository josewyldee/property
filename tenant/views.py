import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.generic import TemplateView
from communications.utils import Util
from communications.models import Email
from maintenance.models import Maintenance
from property.models import Unit
from finance.models import Charges
from .models import Tenant,Guarantors,EmergencyContacts,Lease,LeaseTermination,TenantDocuments
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from customAuth.serializers import RegisterSerializer

from .serializers import TenantSerializer,EmergencyContacts_serializer,Guarantors_serializer,Lease_serializer,Terminate_serializer,Document_serializer
from utils import custom_apiviews,error_loop
from customAuth.models import User
class details(TemplateView):
    template_name = "tenant/detail.html"
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            tenant=get_object_or_404(Tenant, pk=self.kwargs.get('id'))
            maintenance=Maintenance.objects.filter(tenant=tenant)
            try:
                lease=Lease.objects.filter(tenant=tenant,active=True)
                lease=lease[0]
                unit=lease.unit.id
            except:
                lease=None
                unit=None

            context['tenant'] = tenant
            context['account'] =tenant.user
            context['lease'] =lease
            context['unit'] =unit
            context['maintenance'] =maintenance

            return context
class lease_details(TemplateView):
    template_name = "tenant/lease_details.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            lease=get_object_or_404(Lease, pk=self.kwargs.get('id'))
            tenant=Tenant.objects.get(id=lease.tenant.id)
            unit=Unit.objects.get(id=lease.unit.id)
            rent_charges=Charges.objects.filter(id__in=unit.unit_charges)
            print("------------900000000000000")
            print(rent_charges)
            context['tenant'] = tenant
            context['lease'] =lease
            context['unit'] =unit
            context['rent_charges'] =rent_charges
            return context




class tenants(TemplateView):
    template_name = "tenant/index.html"
class buyers(TemplateView):
    template_name = "tenant/buyers.html"
    
class EditDelete_tenant(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()
    success_update='The tenant was updated'
    success_delete='The tenant was deleted'
 
    def get_queryset(self):
        return Tenant.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_tenant(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    success_insert='Your tenants have been added'
    def create(self, request, format=None, *args, **kwargs):
    
        request.data._mutable = True
        allocate_credentials=request.POST.get('allocate_credentials')
        # email_credential=request.POST.get('email_credential')
        # password_credential=request.POST.get('password_credential')
        # password_credential2=request.POST.get('password_credential2')
        # first_name=request.POST.get('name').split()[0]
        # last_name=request.POST.get('name').split()[1]
        request.data['first_name']="none"
        request.data['last_name']="none"
        name=request.POST.get('name')
        if name:
            request.data['first_name']=request.POST.get('name').split()[0]
            if " " in name:
              
                request.data['last_name']=request.POST.get('name').split()[1]
            

        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        request.data['username']=request.POST.get('email').split("@")[0]
        request.data['is_syestem_admin']=False
        request.data['is_tenant']=True
        # print("heeeeeeeeeeeeeeeeeeeeey",request.data)
 
     
       
        the_data=request.data
        many=False
        if allocate_credentials=="is_active":
            serializer = self.get_serializer(data=the_data, many=many)
            serializer_user = RegisterSerializer(data=the_data, many=many)

            if serializer.is_valid():
                if serializer_user.is_valid():
                    
                    saved_user = serializer_user.save(is_syestem_admin=False,is_tenant=True)
                    saved_tenant = serializer.save(added_by=self.request.user,user=saved_user)
                    
                    return Response({
                        'success': self.success_insert,
                        'response': serializer.data,
                    })
                else:
                    error_response=error_loop.fix_errors(serializer_user.errors)
                    # error_response = error_loop.fix_errors(serializer_user.errors)
                    # print("serialiser errors",serializer.errors)
                    print("serialiser USER ",error_response)
                    return Response({
                        'error': error_response
                    })


            else:
                error_response=error_loop.fix_errors(serializer.errors)
                # error_response = error_loop.fix_errors(serializer_user.errors)
                # print("serialiser errors",serializer.errors)
                print("serialiser tenant ",error_response)
                return Response({
                    'error': error_response
                })
        else:
            serializer = self.get_serializer(data=the_data, many=many)

            if serializer.is_valid():
                saved_user2 = serializer.save(added_by=self.request.user)

                return Response({
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
        type=self.request.query_params.get('type')
        data = Tenant.objects.filter(tenant_type=type)
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'phone_number', 'occupancy_status')
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
            emrgency_contact=""
            gurantor_contact=""
            details=""
            if row.tenant_type=="renter":
                emrgency_contact=f'<hr> <a class="dropdown-item edit_person_button" id="{row.id}" >Emergency contacts</a>'
                gurantor_contact=f'<a class="dropdown-item edit_guarantor_button" id="{row.id}" >Edit guarantor details</a>'
                details=f'''<a class="dropdown-item"href="{reverse('tenant:details', kwargs={'id': row.id })}">Open details (New page)</a>'''
            email=f'<span>-------- </span> '
            if row.email:
                email=f'<span >{row.email} </span> '
            if row.phone_number:
                phone=f'<span >{row.calling_code}  {row.phone_number} </span> '
            else:
                phone=f'<span >--------- </span> '
           
            if row.user:
                crede='<span class="badge light badge-danger rounded">Account not active</span>'
                if row.user.is_active:
                    crede='<span class="badge light badge-success rounded">Can login</span>'
            else:
                crede='<span class="badge light badge-secondary rounded">Account not created</span>'
            if row.occupancy_status=="no unit":
              
                status='<span >No lease</span>'

            else:
                status='<span >Lease created</span>'
            data.append([
                row.name,
                phone,
                email,
                
            
                status,
                # crede,
                # crede,
               
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
                    <a class="dropdown-item tenant_info text-primary" id="{row.id}" >Edit</a>

                    <a class="dropdown-item tenant_delete text-primary"  id="{row.id},{row.name}">Delete</a>
                   
                    {emrgency_contact}
                    {gurantor_contact}
                    {details}
                    
                    
                </div>
            </div>''',
            ])
#  
            
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)

class EditDelete_guarantor(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The guarantor was updated successfully'
    success_delete='The guarantor was deleted successfully'
    serializer_class = Guarantors_serializer
    queryset = Guarantors.objects.all()
    def get_queryset(self):
        return Guarantors.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_guarantor(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Guarantors.objects.all()
    serializer_class = Guarantors_serializer
    success_insert='The guarantor has been added'
    def get_queryset(self):
        tenant=self.request.query_params.get('tenant')
        data = Guarantors.objects.filter(tenant=tenant).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'relationship', 'has_accepted')
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
                row.name,
                row.relationship,
                row.has_accepted,
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
                    <a class="dropdown-item edit_guarantor" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_guarantor" id="{row.id},{row.name},{row.tenant.id}" >Delete</a>
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
class EditDelete_emergency(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = EmergencyContacts_serializer
    queryset = EmergencyContacts.objects.all()
    success_update='The emergency contact was updated successfully'
    success_delete='The emergency contact was deleted successfully'
    def get_queryset(self):
        return EmergencyContacts.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
class ListCreate_emergency(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = EmergencyContacts.objects.all()
    serializer_class = EmergencyContacts_serializer
    success_insert='Emergency contact has been added'

    def get_queryset(self):
        tenant=self.request.query_params.get('tenant')
        data = EmergencyContacts.objects.filter(tenant=tenant).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name', 'phone', 'relationship')
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
                row.name,
                row.relationship,
                f'{row.calling_code}  {row.phone}',
                
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
                    <a class="dropdown-item edit_person" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_person" id="{row.id},{row.name},{row.tenant.id}" >Delete</a>
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
    
    
    
    
    
    
    
    
class purchase(TemplateView):
    template_name = "tenant/purchase.html"
    
    
class lease(TemplateView):
    template_name = "tenant/lease.html"
    
    
class EditDelete_lease(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The lease was updated successfully'
    success_delete='The lease was deleted successfully'
    serializer_class = Lease_serializer
    queryset = Lease.objects.all()
    def get_queryset(self):
        return Lease.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_lease(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Lease.objects.all()
    serializer_class = Lease_serializer
    success_insert='The lease has been added'
    
    def create(self, request, format=None, *args, **kwargs):
        # print(request.data.POST.get('tenant'))
        # request.data._mutable = True
        lease_sent=request.POST.get('sent')   
        lease_group=request.POST.get('lease_group')   
        success_insert=self.success_insert
        print(request.data)
        the_data=request.data
        many=False
        # tenant=request.POST.get('tenant')
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            # tenant_data=Tenant.objects.get(id=tenant)
            lease = serializer.save(added_by=self.request.user,active=True)
            id= serializer.data['id']
            lease_info=Lease.objects.get(id=id)
            if lease_group=="purchase":
                lease_sent=request.POST.get('sent') 
                pass

            if lease_sent=="yes":
                email_data=[]
                lease_title=id
                lease=lease_info
                email=lease_info.tenant.email
   
                type_id=lease_title
                # honeypot=receipt_group
                subject="Lease created"

                success=0
                fail=0
                if email:
                    
                    status='sent'
                    reason=None
                    property_name= lease_info.unit.unit_property.property_name
                    info_lease=f'{lease_info.unit.unit_name}, {property_name}'
                    body=f'Thank you for renting with us. You have been allocated {info_lease}. Kindly contact your landlord to get more information such as rental charges, lease information, Payment options, access to the web app among others..'
                    template='email_templates/lease.html'
                    email_data.append({'subject':subject, 'to':email,'from':request.user.email,
                            'name':lease_info.tenant.name,'property':property_name,'body':body,'color':'#4b72fa','template':template,'unit':lease_info.unit.unit_name,'document':None,'lease_type':lease_info.lease_type,'lease_from':lease_info.start_date,'lease_to':lease_info.end_date,'amount':None,'href':None })
                  
                    Util.send_email(email_data)
                    success+=1
                else:
                    status='not sent'
                    reason='email not found'
                    fail+=1
                Email.objects.create(
                lease=lease
                ,email_sent_to=email,body=body,subject=subject
                ,group='lease',type='lease created',type_id=type_id,status=status,document=None
                ,reason=reason,added_by=self.request.user
                
                )
                if fail==0:
                    success_insert='The lease has been created and sent'
                else:
                    success_insert=f'The lease has been created however,the email was not sent due to lack of email address. '

                    

            # Notification.objects.create(notification_type='lease', from_user=request.user, to_user=tenant_data.user, lease=lease)
            


            # property_auto= serializer.data['id']
            # property_name= request.POST.get('property_name')
         
            return Response({
                # 'property_auto': property_auto,
                # 'property_name': property_name,
               
                'success': success_insert,
                'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })

    
    def get_queryset(self):
        type=self.request.query_params.get('type')
        data = Lease.objects.filter(lease_group=type).select_related('tenant','unit').order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'lease_type', 'unit__unit_name','lease_type','tenant__name')
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
  
            if row.tenant.tenant_type=="renter":
                if row.active:
                        status='<span class="badge light badge-success rounded">Active</span>'
                else:
                    status='<span class="badge light badge-danger rounded">Terminated</span>'
                data.append([
                    
                    f''' 
                    <span class="text-left">  
                    {row.tenant.name}
                    <br>
                    {row.unit.unit_name}
                    </span>
                    ''',
                    
                    
                    row.lease_type,
                    f'''   
                <span class="text-bold font-w600"> From:</span> {row.start_date}
                    <br>
                    <br>
                    Till: {row.end_date}
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
                        <a class="dropdown-item edit_lease text-primary" id="{row.id}" >Edit</a>
                         <a class="dropdown-item"href="{reverse('tenant:terminate')}">Terminate lease</a>
                        <hr>
                        <a class="dropdown-item edit_document" id="{row.tenant.id}" >Tenant documents</a>
                        <a class="dropdown-item"href="{reverse('tenant:lease_details', kwargs={'id': row.id })}">Open details (New page)</a>
                    </div>
                </div>''',
                
                
                ])
            else:
                if row.is_paid:
                        status='<span class="badge light badge-success rounded">Payments made</span>'
                        date=row.start_date.strftime("%d %b, %Y")
                else:
                    status='<span class="badge light badge-danger rounded">No payments made</span>'
                    date="-------"
                data.append([
              
                f''' 
                <span class="text-left fancy_text4">  
                {row.tenant.name}
                <br>
                <br>
                {row.unit.unit_name}
                </span>
                ''',
                '{:,}'.format(row.purchase_price),
                
                status,
                date,
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
                        <a class="dropdown-item edit_lease " id="{row.id}" >View details</a>
                        
                    <hr>
                        <a class="dropdown-item edit_document" id="{row.tenant.id}" >View documents</a>
                        <a class="dropdown-item"href="{reverse('tenant:lease_details', kwargs={'id': row.id })}">Open details (New page)</a>
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



class EditDelete_terminate(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The lease was updated successfully'
    success_delete='The lease was deleted successfully'
    serializer_class = Terminate_serializer
    queryset = LeaseTermination.objects.all()
    

    def get_queryset(self):
        return LeaseTermination.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_terminate(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = LeaseTermination.objects.all()
    serializer_class = Terminate_serializer
    success_insert='The termination was succesfull'
    def create(self, request, format=None, *args, **kwargs):
        lease_id=request.POST.get('lease')   
        success_insert=self.success_insert
        print(request.data)
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            lease = serializer.save(added_by=self.request.user)
            id= serializer.data['id']
            reason= serializer.data['reason']
            date= serializer.data['date']
            description= serializer.data['description']
            lease_info=Lease.objects.get(id=lease_id)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(lease_info)
            print("IDDDDDDDDDD",id)
            email_data=[]
            lease_title=id
            lease=lease_info
            email=lease_info.tenant.email
            type_id=lease_title
            # honeypot=receipt_group
            subject="Lease termination"

            success=0
            fail=0
            property_name= lease_info.unit.unit_property.property_name
            body=f'  Please be advised that your {lease_info.lease_type} tenancy for {lease_info.unit.unit_name} in {property_name} has been terminated. Below you will find the reason why.'
            if email:
                
                status='sent'
                
                template='email_templates/lease_termination.html'
                email_data.append({'subject':subject, 'to':email,'from':request.user.email,
                        'name':lease_info.tenant.name,'property':property_name,'body':body,'color':'#4b72fa','template':template,'unit':lease_info.unit.unit_name,'document':None,'lease_type':lease_info.lease_type,'lease_from':date,'reason':reason ,'description':description,'amount':None})
                
                Util.send_email(email_data)
                success+=1
            else:
                status='not sent'
                reason='email not found'
                fail+=1
            Email.objects.create(
            lease=lease
            ,email_sent_to=email,body=body,subject=subject
            ,group='lease',type='lease termination',type_id=type_id,status=status,document=None
            ,reason=reason,added_by=self.request.user
            
            )
            if fail==0:
                success_insert='The lease has been terminated and the tenanat has been notified by email.'
            else:
                success_insert=f'The lease has been terminated however,an email was not sent due to lack of an email address. '

                

            # Notification.objects.create(notification_type='lease', from_user=request.user, to_user=tenant_data.user, lease=lease)
            


            # property_auto= serializer.data['id']
            # property_name= request.POST.get('property_name')
         
            return Response({
                # 'property_auto': property_auto,
                # 'property_name': property_name,
               
                'success': success_insert,
                'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })
    def get_queryset(self):
        data = LeaseTermination.objects.select_related('lease').all().order_by('-added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'reason', 'lease.tenant.name', 'lease.unit.unit_name')
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
            data.append([

                f'''   
                <span class="text-left">
                {row.lease.tenant.name}
                <br>
                 {row.lease.unit.unit_name}
                 </span>
                ''',

                row.lease.lease_type,
                row.reason,
                row.date,
             
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
                    <a class="dropdown-item edit_termination" id="{row.id}" >View</a>
                    <a class="dropdown-item edit_document" id="{row.lease.tenant.id}" >Tenant documents</a>
                   
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
    


class terminate(TemplateView):
    template_name = "tenant/terminate.html"

class EditDelete_documents(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = Document_serializer
    queryset = TenantDocuments.objects.all()
    success_update='The photo was updated'
    success_delete='The photo was deleted'

    def get_queryset(self):
        return TenantDocuments.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_documents(custom_apiviews.ListCreateAPIView):

    data = []
    queryset = TenantDocuments.objects.all()
    serializer_class = Document_serializer
    success_insert='Your document has been added'
    

    def get_queryset(self):
        tenant=self.request.query_params.get('tenant')
        data = TenantDocuments.objects.filter(tenant=tenant).order_by('-added_on')
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
        filtered_queryset = self.filter_for_datatable(queryset)
        data = []
        row_data = filtered_queryset
        for row in row_data:
           data.append ([
                f'''<svg id="icon-orders" xmlns="http://www.w3.org/2000/svg"
                                                            width="30" height="30" viewBox="0 0 24 24" fill="none"
                                                            stroke="currentColor" stroke-width="2"
                                                            stroke-linecap="round" stroke-linejoin="round"
                                                            class="feather feather-file-text">
                                                            <path
                                                                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
                                                            </path>
                                                            <polyline points="14 2 14 8 20 8"></polyline>
                                                            <line x1="16" y1="13" x2="8" y2="13"></line>
                                                            <line x1="16" y1="17" x2="8" y2="17"></line>
                                                            <polyline points="10 9 9 9 8 9"></polyline>
                                                        </svg>''',
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
                        <a class="dropdown-item" href="{row.document.url}" id="{row.id}">Download</a>
                        <a class="dropdown-item delete_doc_button" id="{row.id}">Delete</a>
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
    

def test_this(self):
    
    current_date=datetime.date.today() + datetime.timedelta(days=7)
    print("thhhhhhhhhhhhhhhe",current_date)
    # doc1=TenantDocuments.objects.get(id=1)
    # document=doc1.document
    # try:
    #     doc=TenantDocuments.objects.get(document=document)
    # except:
    #     doc=None
    # if doc is not None:
    #     print("proccccccccccceeed",doc1.created_at)


    # print("doooooooooooooooooooooocemnet")
    # print(doc.document.url)
    # for i in doc:
    #     print (i.document.url)
    