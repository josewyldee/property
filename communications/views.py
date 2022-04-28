from rest_framework.response import Response
from django.views.generic import TemplateView
from .utils import Util
from django.contrib.postgres.search import SearchVector
# from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from utils.bulk_insert import bulk_data_fomart
from django.template.loader import get_template,render_to_string
from utils import custom_apiviews,error_loop
from .serializers import EmailSerializers,Email
from tenant.models import Lease

# Create your views here.
class email(TemplateView):
    
    template_name = "communications/email.html"



def send_email(request,email,name,subject,body,type,property,document,template):
 
    # user = Tenant.objects.all()
    # print(user.email)
   
    # current_site =  request.META['HTTP_HOST']
    # relativeLink = reverse('property:dashboard')
    # absurl = 'http://'+current_site+relativeLink+"?token="+'what is the point of having f you money'
    # email_body = 'Hi '+user.name + \
    #     ' Use the link below to verify your email \n ' + absurl

    
    data=[]
    # for row in user:
    #     email_body = 'Hi '+row.name + \
    #     ' Use the link below to verify your email \n ' + absurl
    data.append({'subject':subject,'body': body, 'to':email,'from':request.user.email,
            'name':name,'property':property,'document':document,'template':template,'color':'#4b72fa','amount':0,'href':'#'})
    # print(absurl)
    

    Util.send_email(data)
    return 'success'


class EditDelete_emails(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = EmailSerializers
    queryset = Email.objects.all()
    success_update='The email was updated'
    success_delete='The email was deleted'

    def get_queryset(self):
        return Email.objects.all()


    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_emails(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Email.objects.all()
    serializer_class = EmailSerializers
    success_insert='Your email has been sent'
    def create(self, request, format=None, *args, **kwargs):
        unit_list=request.POST.get('unit_list').split(",") 
        subject=request.POST.get('subject')
        body=request.POST.get('body')
        type=request.POST.get('type')
        raw_document=request.FILES.getlist('document')
        request.data._mutable = True
        
   
   
        doc=None
        document=[]
        if request.data['document']:
            # request.data['document']=request.FILES['document']
            doc=request.FILES['document']
            request.data['document']=doc
            for f in raw_document:
                document.append({'name':f.name,'read':f.read(),'type':f.content_type})
        else:
            request.data['document']=None
        success=0
        fail=0
        unit_list=[int(i) for i in unit_list]
        request.data._mutable = True
        
       
        raw_data=bulk_data_fomart(request.data)
        many = isinstance(raw_data, list)
        serializer = self.get_serializer(data=raw_data, many=many)
        leases=Lease.objects.filter(id__in=unit_list).select_related('tenant','unit__unit_property')
        if serializer.is_valid():
            data=serializer.data
            for row in leases:
                lease=row
                name=row.tenant.name
                email=row.tenant.email
                property=row.unit.unit_property.property_name
                for child_row in data:
                    print("9999999999999999999999999999999999999999")
                    child_row['document']=doc
                    print(child_row['document'])
                    if email:
                        template='email_templates/message.html'
                        send_email(request,email,name,subject,body,type,property,document,template)
                        child_row['status']='sent'
                        child_row['reason']=None
                        success+=1
                    else:
                        child_row['status']='not sent'
                        child_row['reason']='email not found'
                        fail+=1
                    Email.objects.create(
                    lease=lease
                   ,email_sent_to=email,body=body,subject=subject
                    ,type=child_row['type'],status=child_row['status'],document=child_row['document']
                    ,reason=child_row['reason'],added_by=self.request.user
                    
                    )
            
            if fail==0:
                msg='All the emails have been sent and stored in the database'
            else:
                msg=f'Data saved successfully however, {fail} emails were not sent due to lack of email address. '
            return Response({
                
                'success': msg,
            })
        else:
            error_response = error_loop.fix_errors_bulk(serializer.errors)
            print("serialiser errors",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        # print(self.request.user.user_type)
        data=Email.objects.all().select_related('lease','lease__unit','lease__tenant','lease__unit__unit_property','added_by')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'subject','lease__tenant__name', 'lease__unit__unit_name')
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
                 
                f'''   
                {row.lease.tenant.name}
                <br>
                   {row.lease.unit.unit_name}
            
                ''',
                row.group,
                row.subject,
                 f'''   
                {row.added_by.username}
                <br>
                   {row.added_on.strftime("%d %b, %Y")}
                <br>
                   {row.added_on.strftime("%d %b, %Y")}
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
<a class="dropdown-item view_email text-primary" id="{row.id}">View email</a>
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

def test(self):
    html_content = render_to_string('email_templates/message.html', {'name': 'joseph ddd'})


