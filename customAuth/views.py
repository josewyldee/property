from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import User,AdminProfile
from tenant.models import Tenant
from tenant.serializers import TenantSerializer
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from .serializers import AdminProfileSerializers
from utils import custom_apiviews,error_loop
from customAuth.serializers import RegisterSerializer
from django.shortcuts import get_object_or_404

class profile(TemplateView):
    template_name = "customAuth/profile.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            profile=get_object_or_404(AdminProfile, pk=self.kwargs.get('id'))
           
  
            context['profile'] = profile

            return context  

class admin(TemplateView):
    
    template_name = "customAuth/admin.html"


class EditDelete_admin_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminProfileSerializers
    queryset = AdminProfile.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        id=request.POST.get('user_id')   
        password=request.POST.get('password_credential1')   
        is_active=request.POST.get('is_active')   
        print("hhhhhhhhhhh",is_active)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            usr = User.objects.get(id=id)
            if password !="no_password":
                usr.set_password(password)
            usr.is_active=is_active
            usr.save()
           
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        user_data=request.POST.get('user')   
       
        instance = self.get_object()
        self.perform_destroy(instance)
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return AdminProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_admin_profile(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializers
    success_insert='Your Profile has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        request.data['username']=request.POST.get('email').split("@")[0]
        print("heeeeeeeeeeeeeeeeeeeeey",request.data)

        the_data=request.data
        many=False
      
        serializer = self.get_serializer(data=the_data, many=many)
        serializer_user = RegisterSerializer(data=the_data, many=many)
    
        if serializer.is_valid():
            if serializer_user.is_valid():
                
                saved_user = serializer_user.save(is_employee=False,is_syestem_admin=True,is_tenant=False,added_by=self.request.user)
                saved_profile = serializer.save(added_by=self.request.user,user=saved_user)
                
                return Response({
                    'success': self.success_insert,
                    'response': serializer.data,
                })
            else:
                error_response=error_loop.fix_errors(serializer_user.errors)
                print("serialiser USER ",error_response)
                return Response({
                    'error': error_response
                })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            print("serialiser profile ",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        data = AdminProfile.objects.select_related('user').filter(user__is_syestem_admin=True).order_by('name')
        # data = AdminProfile.objects.select_related('user').all().order_by('name')
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
            if row.user.is_active:
                crede='<span class="badge light badge-success rounded">Can login</span>'
            else:
                crede='<span class="badge light badge-danger rounded">Not active</span>'

            data.append([
                row.name,
                row.user.email,
                row.user.is_syestem_admin,
                crede,
             
               
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
                   
                    <a class="dropdown-item admin_edit text-primary" id="{row.id}" >Edit admin details</a>
                    <a class="dropdown-item admin_delete text-primary"  id="{row.id},{row.name},{row.user.id}">Delete admin</a>
                  

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

        

    
class employee(TemplateView):
    
    template_name = "customAuth/employee.html"


class EditDelete_employee_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AdminProfileSerializers
    queryset = AdminProfile.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        id=request.POST.get('user_id')   
        password=request.POST.get('password_credential1')   
        is_active=request.POST.get('is_active')   
        print("hhhhhhhhhhh",is_active)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            usr = User.objects.get(id=id)
            if password !="no_password":
                usr.set_password(password)
            usr.is_active=is_active
            usr.save()
           
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def destroy(self, request, *args, **kwargs):
        user_data=request.POST.get('user')   
       
        instance = self.get_object()
        self.perform_destroy(instance)
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return AdminProfile.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_employee_profile(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializers
    success_insert='Your Profile has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        request.data['username']=request.POST.get('email').split("@")[0]
        print("heeeeeeeeeeeeeeeeeeeeey",request.data)

        the_data=request.data
        many=False
      
        serializer = self.get_serializer(data=the_data, many=many)
        serializer_user = RegisterSerializer(data=the_data, many=many)
    
        if serializer.is_valid():
            if serializer_user.is_valid():
                
                saved_user = serializer_user.save(is_employee=True,is_syestem_admin=False,is_tenant=False,added_by=self.request.user)
                saved_profile = serializer.save(added_by=self.request.user,user=saved_user)
                
                return Response({
                    'success': self.success_insert,
                    'response': serializer.data,
                })
            else:
                error_response=error_loop.fix_errors(serializer_user.errors)
                print("serialiser USER ",error_response)
                return Response({
                    'error': error_response
                })
        else:
            error_response=error_loop.fix_errors(serializer.errors)
            print("serialiser profile ",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
      
        data = AdminProfile.objects.select_related('user').filter(user__is_employee=True,user__is_syestem_admin=False).order_by('name')
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
            if row.user.is_active:
                crede='<span class="badge light badge-success rounded">Can login</span>'
            else:
                crede='<span class="badge light badge-danger rounded">Not active</span>'

            data.append([
                row.name,
                row.user.email,
                row.user.is_employee,
                crede,
             
               
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
                   
                    <a class="dropdown-item admin_edit text-primary" id="{row.id}" >Edit</a>
                    <a class="dropdown-item admin_delete text-primary"  id="{row.id},{row.name},{row.user.id}">Delete</a>
                  

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

        


    


    
class tenant(TemplateView):
    
    template_name = "customAuth/tenant.html"


class EditDelete_tenant_profile(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()
    success_update='The profile was updated'
    success_delete='The profile was deleted'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print("serrrrrrrrrrr",serializer)
        user_data=User.objects.get(id=serializer.data['user'])
        serializer_user = RegisterSerializer(data=user_data, many=False)
        # print("heeeeeeeeeeey")
        # print(serializer_user.initial_data.email)
        return Response({
                'profile': serializer.data,
                "email":serializer_user.initial_data.email,
                "is_active":serializer_user.initial_data.is_active,
              
            })
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
      
        id=request.POST.get('user_id')   
        password=request.POST.get('password_credential1')   
        is_active=request.POST.get('is_active')   
      
        usr = User.objects.get(id=id)
        if password !="no_password":
            usr.set_password(password)
        usr.is_active=is_active
        usr.save()
        
        return Response({
            'success': self.success_update,
         
        })
      
    def destroy(self, request, *args, **kwargs):
        user_data=request.POST.get('user')   
       
        instance = self.get_object()
        self.perform_destroy(instance)
        u = User.objects.get(id=user_data)
        u.delete()

        return Response({
                'success': self.success_delete,
              
            })

    def perform_destroy(self, instance):
        instance.delete()
      

    def get_queryset(self):
        return Tenant.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_tenant_profile(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    success_insert='Your Profile has been added'
    def create(self, request, format=None, *args, **kwargs):
        request.data._mutable = True
        request.data['password']=request.POST.get('password_credential1')
        request.data['password2']=request.POST.get('password_credential2')
        is_active=request.POST.get('is_active')
        tenant=request.POST.get('tenant')
        request.data['username']=request.POST.get('email').split("@")[0]

        the_data=request.data
        many=False
      
        serializer_user = RegisterSerializer(data=the_data, many=many)
    

        if serializer_user.is_valid():
            
            saved_user = serializer_user.save(is_employee=False,is_syestem_admin=False,is_tenant=True,is_active=is_active,added_by=self.request.user)
            ten = Tenant.objects.get(id=tenant)
            ten.user=saved_user
            ten.save()
        
            
            return Response({
                'success': self.success_insert,
                # 'response': serializer.data,
            })
        else:
            error_response=error_loop.fix_errors(serializer_user.errors)
            print("serialiser USER ",error_response)
            return Response({
                'error': error_response
            })
   

    def get_queryset(self):
      
        data = Tenant.objects.select_related('user').all().order_by('name')
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
            if row.user:
                username=row.user.username
                if row.user.is_active:
                    crede='<span class="badge light badge-success rounded">Can login</span>'
                else:
                    crede='<span class="badge light badge-danger rounded">Not active</span>'
                button='block'
            else:
                crede='<span class="badge light badge-danger rounded">Account not created</span>'
                username="----------------"
                button='d-none'


            data.append([
                row.name,
                username,
             
                crede,
             
               
                f'''
                <div class="dropdown float-right {button} ">
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
                   
                    <a class="dropdown-item admin_edit text-primary" id="{row.id}" >Edit tenant credentials</a>
                  

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

