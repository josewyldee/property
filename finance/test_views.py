from rest_framework.response import Response
from django.views.generic import TemplateView

from tenant.models import Lease
from .models import Charges,Invoice,Receipt, statement
from property.models import Unit
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from utils.bulk_insert import bulk_data_fomart
from .utils import generate_transaction_id
from django.db.models import Sum,Count
from .serializers import ChargeSerializers,InvoiceSerializers,ReceiptSerializers
from utils import custom_apiviews,error_loop
import json,datetime,random
# import datetime





# class dashboard(TemplateView):
    
#     template_name = "property/dashboard.html"
    
class receipt(TemplateView):
    
    template_name = "finance/receipt.html"
    
class invoice(TemplateView):
    
    template_name = "finance/invoice.html"
    
    
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

    data = []
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers
    success_insert='Your invoice has been added'
    # def post(self, request, *args, **kwargs):
    #   unit_list=request.POST.get('unit_list')
    #   lease = Lease.objects.filter(unit__in=unit_list)
      
    # #   print(request.data)

    #   for item in lease:
    #     print(item)
         
    #     for row in request.data:
    #             print("$$$$$$$$$$$$$$$$$$$$$44")
                
    #             row["tenant"] = 'hello'
    #             row["unit"] = 'world'


    #   return super(ListCreate_invoice, self).post(request, *args, **kwargs)
    def create(self, request, format=None, *args, **kwargs):
        unit_list=request.POST.get('unit_list').split(",") 
        
        # property_type = raw_data.split(',')[0]
        # property_category = raw_data.split(',')[1]
        request.data._mutable = True
        
        invoice_group_bulk=generate_transaction_id()
        request.data['invoice_group_bulk']=invoice_group_bulk
        # request.data['property_type']=property_type
        # request.data['property_category']=property_category
    
       
        raw_data=bulk_data_fomart(request.data)
        many = isinstance(raw_data, list)
        serializer = self.get_serializer(data=raw_data, many=many)
        tenants=Lease.objects.filter(unit__in=unit_list).select_related('unit','tenant')
    
        if serializer.is_valid():
            print('------------------------------------------------------')
            # print(serializer.data)
           
            data=serializer.data
          
            for row in tenants:
                lease=row.id
                tenant=row.tenant
                unit=row.unit
                unit_property=row.unit.unit_property
                total_amount=0
            
                invoice_group=f'INV{lease}{invoice_group_bulk}'
                instance=statement.objects.create(statement_invoice=invoice_group,type='invoice',amount=total_amount)
                # statement_instance=instance.statement_invoice
                for child_row in data:
                    child_row['tenant']=tenant
                    child_row['unit']=unit
                    child_row['property']=unit_property
                    # print('------------------------------------------------------')
                    # print(invoice_group_bulk)
                    # print(invoice_group)
                    total_amount+=child_row['amount']
                
                    if child_row['late_fee_amount'] > 0:
                        child_row['deadline_date'] = datetime.date.today() + datetime.timedelta(days=child_row['late_fee_grace'])
                   
                    

                    Invoice.objects.create(added_on=child_row['added_on']
                    ,tenant=child_row['tenant'],unit=child_row['unit']
                    ,invoice_group=instance,invoice_group_bulk=child_row['invoice_group_bulk']
                    ,property=child_row['property'],name=child_row['name']
                    ,amount=child_row['amount'],communication=child_row['communication']
                    ,description=child_row['description'],deadline=child_row['deadline']
                    ,late_fee_category=child_row['late_fee_category'],deadline_date=child_row['deadline_date']
                    ,late_fee_type=child_row['late_fee_type'],late_fee_grace=child_row['late_fee_grace']
                    ,late_fee_date=child_row['late_fee_date'],late_fee_max=child_row['late_fee_max']
                    ,late_fee_amount=child_row['late_fee_amount']
                    
                    )
                
                # serializer.save(added_by=self.request.user,tenant=row.tenant,unit=row.unit,property=row.unit.unit_property)


            # print(serializer.data)
            
            print('------------------------------------------------------')
            # print(final_data)

            # serializer.saved(added_by=self.request.user)

            # property_auto= serializer.data['id']
            # property_name= request.POST.get('property_name')
         
            # return Response({
                
            #     'response': serializer.data,
            #     'success': self.success_insert,
            # })
        else:
            error_response = error_loop.fix_errors_bulk(serializer.errors)
            print("serialiser errors",error_response)
            return Response({
                'error': error_response
            })

    def get_queryset(self):
        # print(self.request.user.user_type)
        # data=Invoice.objects.all().annotate(ni=Count('invoice_group')).order_by()
        # data=Invoice.objects.all().select_related('invoice_group').annotate(ni=Count('invoice_group')).order_by()
        data=Invoice.objects.values('invoice_group').annotate(Count('invoice_group')).order_by()
        # tesy=invoice.obje
        print('-----------------------------------------')
        print(data.query)
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'tenant__name','unit__unit_name')
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
            

            # status=f'<span class="badge light rounded badge-danger">Not paid</span>'
            # if row.amount <=  row.amount_sorted:
            #     status=f'<span class="badge light badge-success">Paid</span>'
            # if row.amount_sorted >0:
            #     status=f'<span class="badge light badge-primary">Partially paid</span>'
            

            data.append ([
            #    row.ni,
            #   row.invoice_group.id,
                row.amount,
                f'''   
                {row.tenant.name}
                <br>
                 {row.unit.unit_name}
                <br>
                 {row.property.property_name}
                ''',
                
              
           
              
            #    f''' 
            #     <div class="dropdown float-right">
            #         <button type="button"
            #             class="btn btn-primary light sharp btn-rounded"
            #             data-toggle="dropdown" aria-expanded="false">
            #             <svg width="20px" height="20px" viewBox="0 0 24 24"
            #                 version="1.1">
            #                 <g stroke="none" stroke-width="1" fill="none"
            #                     fill-rule="evenodd">
            #                     <rect x="0" y="0" width="24" height="24"></rect>
            #                     <circle fill="#000000" cx="5" cy="12" r="2"></circle>
            #                     <circle fill="#000000" cx="12" cy="12" r="2"></circle>
            #                     <circle fill="#000000" cx="19" cy="12" r="2"></circle>
            #                 </g>
            #             </svg>
            #         </button>
            #         <div class="dropdown-menu" x-placement="bottom-start"
            #             style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 40px, 0px);">
                       
            #             <a class="dropdown-item edit_property_button text-primary" id="{row.id}">View</a>
            #              <hr>
            #             <a class="dropdown-item" href="{reverse('property:details', kwargs={'property': row.id })}">Property details (New page)</a>
            #             <a class="dropdown-item" href="{reverse('property:units', kwargs={'property': row.id })}">Open units (New page)</a>

            #         </div>
            #     </div>
            #    ''',
               
             
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data
        }
        return Response(response)


