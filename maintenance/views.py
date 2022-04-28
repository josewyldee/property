from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.generic import TemplateView

from notifications.models import Notification
from .models import Maintenance,Cost,Document
from tenant.models import Tenant,Lease
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from .serializers import MaintenanceSerializers,CostSerializers,DocumentSerializers
from utils import custom_apiviews,error_loop
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db.models import Sum,OuterRef, Subquery,Count
from django.db.models.functions import Coalesce
# import datetime
from datetime import datetime
class index(TemplateView):
    template_name = "maintenance/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type=self.request.user.is_tenant

        if user_type:
            tenant=Tenant.objects.get(user=self.request.user.id)
            lease=Lease.objects.filter(tenant=tenant.id)
            if lease:
                context['lease'] =lease[0]
            context['tenant'] =tenant
            context['base_template'] = 'base.html'
        else:
            context['base_template'] = 'base.html'
        return context

class details(TemplateView):
    
    template_name = "maintenance/details.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['main'] = get_object_or_404(Maintenance, pk=self.kwargs.get('maintenance'))
        
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
        # tenant_data=Tenant.objects.get(id=tenant)
        # notification_for=tenant_data.user
        if request.user.is_tenant:
             request.data['added_by_category']='tenant'


        # print("te=aaaarget",tenant_data.name)
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            maintenance = serializer.save(added_by=self.request.user)
            id= serializer.data['id']
            # Notification.objects.create(notification_type='maintenance', from_user=request.user, to_user=notification_for, maintenance=maintenance)
            return Response({
                'id': id,
                'success': self.success_insert,
            })
        else:
            error_response = error_loop.fix_errors(serializer.errors)
            print("serialiser errors",serializer.errors)
            return Response({
                'error': error_response
            })
    def get_queryset(self):
        if self.request.user.is_syestem_admin:
            data = Maintenance.objects.select_related('tenant','unit').all()
        elif self.request.user.is_employee:
            data = Maintenance.objects.select_related('tenant','unit').all()
        else:
            # request.session['tenant'] = tenant.id
            tenant=Tenant.objects.get(user=self.request.user.id)
            data = Maintenance.objects.select_related('tenant','unit').filter(tenant=tenant.id)

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

        if request.user.is_tenant:
            class_variable="d-none"
        else:
            class_variable="hello-world"

     
        for row in row_data:
            status=f'<span class="badge light badge-success btn-rounded px-4">Complete</span>'
            if row.status=="in progress":
                status=f'<span class="badge light badge-primary btn-rounded px-4">In progress</span>'
            if row.status=="not started":
                status=f'<span class="badge light badge-danger btn-rounded px-4">Not started</span>'
            if row.reported_on:
                reported_on= f'''          
                   <span class="text-bold text-primary">Reported on: </span><br>({row.reported_on.strftime("%Y-%m-%d")})<br>({row.since} days ago)
                  '''
            else:
                reported_on="---------"
            
            data.append([
                  f'''          
                    {row.tenant.name}<br>{row.unit.unit_name}
                  ''',
                  row.name,
                 reported_on,
                    row.priority,
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
                 
                    <a class="dropdown-item edit_maintenance " id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_maintenance  {class_variable}" id="{row.id},{row.name}" >Delete</a>
                      <hr>
                    <a class="dropdown-item cost_button {class_variable}" id="{row.id}" >View costs</a>
                    <a class="dropdown-item attach_photos" id="{row.id}" >View photos</a>
                      <hr>
                    <a class="dropdown-item" href="{reverse('maintenance:details', kwargs={'maintenance': row.id })}">Details (New page)</a>
                  
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


class EditDelete_cost(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    success_update='The cost was updated successfully'
    success_delete='The cost was deleted successfully'
    serializer_class = CostSerializers
    queryset = Cost.objects.all()
    def get_queryset(self):
        return Cost.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_cost(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Cost.objects.all()
    serializer_class = CostSerializers
    success_insert='The cost has been added'
    def get_queryset(self):
        maintenance=self.request.query_params.get('maintenance')
        data = Cost.objects.filter(maintenance=maintenance).order_by('added_on')
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'cost_type', 'cost_name', 'paid_by')
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
                   f'''          
            {row.cost_type}<br>({row.cost_name})
                  ''',
                row.cost_total,
                row.paid,
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
                    <a class="dropdown-item edit_cost text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item remove_cost text-primary" id="{row.id},{row.maintenance.id}" >Delete</a>
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
        data = Document.objects.filter(maintenance=maintenance).order_by('added_on')
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
                    <a class="dropdown-item download_document " href="{row.document.url}" id="{row.id}" >Download</a>
                    <a class="dropdown-item remove_document" id="{row.id},{row.maintenance.id}" >Delete</a>
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


      
