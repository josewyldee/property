from datetime import date,datetime,timedelta
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import Property, Property_documents,Unit,Unit_features,Unit_photos, Utility_bills
from maintenance.models import Maintenance
from tenant.models import Lease

from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.db.models import Q , Count,Sum,OuterRef, Subquery,F
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from utils.bulk_insert import bulk_data_fomart_decision
from django.shortcuts import get_object_or_404
from .serializers import DocumentSerializers, PropertySerializers,UnitSerializers,FeaturesSerializers,PhotoSerializers,UtilitySerializers
from utils import custom_apiviews,error_loop
from django.http import Http404,HttpResponse
import json
from django.contrib.humanize.templatetags.humanize import ordinal

class construction(TemplateView):
    
    template_name = "property/sorry.html"
    


def units_filter(request):
    
    occupied = Count('occupancy_status', filter=Q(occupancy_status="occupied"))
    vacant = Count('occupancy_status', filter=Q(occupancy_status="vacant"))
   
    pubs = Unit.objects.annotate(vacant=vacant).annotate(occupied=occupied)
    pubs[0].occupied
    pubs[0].vacant
    vacant=0
    occupied=0
    context=[] 
    for i in range(0,len(pubs)):
        vacant+=pubs[i].vacant
        occupied+=pubs[i].occupied

    # context['vacant'] =vacant
    # context['occupied'] =occupied
 
    return vacant,occupied
class dashboard(TemplateView):
    
    template_name = "property/dashboard.html"
    
    def get_context_data(self, **kwargs):
        from finance.models import Expense,Statement,Invoice
        all_units= Unit.objects.all()
    # expenses =Expense.objects.annotate(amount=Sum(Subquery(
    #         Expense.objects.filter(expense_name=OuterRef('expense_name')).values('expense_name').annotate(total_amount=Sum(OuterRef('amount'))).values('total_amount')[:1]
    #      ))).exclude("amount")
        from django.db.models.functions import TruncMonth
        year=datetime.now().year
        query=Statement.objects.filter(created_on__year=year).annotate(month=TruncMonth('created_on')).values('month').annotate(total_amount=Sum('amount')).values("month","total_amount","type")
        # late_invoices=Invoice.objects.filter(invoice_type="invoice",is_cancelled=False,late_fee_amount__gt=0).order_by('created_on')
        late_invoices=Invoice.objects.annotate(total_amount=Sum(F('amount')-F('amount_sorted'))).filter(invoice_type="invoice",is_cancelled=False,late_fee_amount__gt=0,total_amount__gt=0).order_by('created_on')

        invoice_months ={'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}
        payment_months={'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0}
        invoice_query=query.filter(Q(type="invoice")|Q(type="credit note"))
        payment_query=query.filter(Q(type="payment")|Q(type="debit note"))
        total_invoice=0
        total_payment=0
        for row in invoice_query:
            total_invoice+=row["total_amount"]
            invoice_months.update({row["month"].strftime("%b"):row["total_amount"]})
        for row in payment_query:
            total_payment+=row["total_amount"]
            payment_months.update({row["month"].strftime("%b"):row["total_amount"]})
        
        expenses=Expense.objects.values('expense_name').annotate(total_amount=Sum('amount')).values("expense_name","total_amount")

        all_lease=Lease.objects.filter(lease_type="fixed period",active=True,end_date__gte=datetime.today())
    
        thirty_days = all_lease.filter(end_date__lt=datetime.today()+timedelta(days=30))
        count_thirty=thirty_days.count()
        sixty_days = all_lease.filter(end_date__lt=datetime.today()+timedelta(days=60))
        count_sixty=sixty_days.count()
        ninty_days = all_lease.filter(end_date__lt=datetime.today()+timedelta(days=90))
        count_ninty=ninty_days.count()

        occupied_units=all_units.filter(occupancy_status="occupied").count()
        vacant_units=all_units.filter(occupancy_status="vacant").count()
        occupied_units=all_units.filter(occupancy_status="occupied").count()
        vacant_units=all_units.filter(occupancy_status="vacant").count()
        unit_count=all_units.count()
        property_location=Property.objects.values('country').annotate(count_property=Count('id'))
      
        country_codes=Property.objects.values('country_code')
      
        # property_location=all_units.values('unit_property__country').annotate(dcount=Count('unit_property__country'))
        # country_codes=all_units.values('unit_property__country_code').annotate(dcount=Count('unit_property__country_code'))

        print("++++++++++++++++++++++++++++++++++")
        print(country_codes)
        context = super().get_context_data(**kwargs)
        context['maintenance'] = Maintenance.objects.all()
        context['property_count'] =Property.objects.all().count()
        context['unit_count'] =unit_count
        context['late_invoices'] =late_invoices
        context['invoice_months'] =invoice_months
        context['payment_months'] =payment_months
        context['expenses'] =expenses
        context['total_invoice'] =total_invoice
        context['total_payment'] =total_payment
        context['thirty_days'] =thirty_days
        context['count_thirty'] =count_thirty
        context['sixty_days'] =sixty_days
        context['count_sixty'] =count_sixty
        context['ninty_days'] =ninty_days
        context['count_ninty'] =count_ninty
        context['recent_property'] =all_units[:3]
        context['all'] =all_units
        
        context['occupied_units'] =occupied_units
        context['vacant_units'] =vacant_units
    
        context['property_location'] =property_location 
        context['country_codes'] =country_codes 
    
        return context
   

    
    
class property(TemplateView):
    
    template_name = "property/property.html"

class property_detail(TemplateView):
    
    template_name = "property/property_detail.html"
    
    def get_context_data(self, **kwargs):
            from finance.models import Invoice,Expense
            context = super().get_context_data(**kwargs)
            context['property'] = get_object_or_404(Property, pk=self.kwargs.get('property'))
            property=self.kwargs.get('property')

            subquery_income = Invoice.objects.filter(
            lease__unit__unit_property=property,is_cancelled=False
            ).aggregate(
                total_income = Sum('amount_sorted')
            )

            subquery_expense = Expense.objects.filter(
            property=property
            ).aggregate(
                total_expense = Sum('amount')
            )
            print("++++++++++++++++++++++++++")
            total_income=0
            total_expense=0
            if subquery_income['total_income']:
                total_income=subquery_income['total_income']
            if subquery_expense['total_expense']:
                total_expense=subquery_expense['total_expense']
            
            earnings=total_income+total_expense
            if earnings !=0:
                total_percent=(total_income/earnings)*100
                total_percent=format(total_percent, ".2f") 
            else:
                total_percent=0
            context['total_income'] =total_income
            context['total_expense'] =total_expense
            context['total_percent'] =total_percent
            context['units'] = Unit.objects.filter(unit_property=self.kwargs.get('property'))
            context['documents'] = Property_documents.objects.filter(property=self.kwargs.get('property'))
            context['utility'] = Utility_bills.objects.filter(property=self.kwargs.get('property'))
        
            return context
class unit_detail2(TemplateView):
    
    template_name = "property/unit_detail2.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            records=Unit.objects.get(id=self.kwargs.get('unit'))
            context['unit'] = records
            context['lease'] = Lease.objects.filter(unit=self.kwargs.get('unit')).first()
            context['maintenance'] = Maintenance.objects.filter(unit=self.kwargs.get('unit'))
            features_list=[]
            photos_list=[]
            charges_list=[]
            if records.unit_features:
                features_list=records.unit_features
            
            if records.unit_photos:
                photos_list=records.unit_photos
            if records.unit_charges:
                charges_list=records.unit_charges
            
            features_list=[int(i) for i in features_list]
            photos_list=[int(i) for i in photos_list]
            charges_list=[int(i) for i in charges_list]
            print("features_list",features_list)
            print("photos_list",photos_list)
            print("charges_list",charges_list)
    
            context['features_list'] = features_list
            context['photos_list'] =photos_list
            context['charges_list'] =charges_list
            return context
class unit_detail(TemplateView):
    
    template_name = "property/unit_detail.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            records=Unit.objects.get(id=self.kwargs.get('unit'))
            context['unit'] = records
            context['lease'] = Lease.objects.filter(unit=self.kwargs.get('unit')).first()
            context['maintenance'] = Maintenance.objects.filter(unit=self.kwargs.get('unit'))
            features_list=[]
            photos_list=[]
            charges_list=[]
            if records.unit_features:
                features_list=records.unit_features
            
            if records.unit_photos:
                photos_list=records.unit_photos
            if records.unit_charges:
                charges_list=records.unit_charges
            
            features_list=[int(i) for i in features_list]
            photos_list=[int(i) for i in photos_list]
            charges_list=[int(i) for i in charges_list]
            print("features_list",features_list)
            print("photos_list",photos_list)
            print("charges_list",charges_list)
    
            context['features_list'] = features_list
            context['photos_list'] =photos_list
            context['charges_list'] =charges_list
            return context
class units(TemplateView):
    
    template_name = "property/units.html"
    
    def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            if self.kwargs.get('property'):
                context['property'] = get_object_or_404(Property, pk=self.kwargs.get('property'))
        
            return context

class EditDelete_property(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = PropertySerializers
    queryset = Property.objects.all()
    success_update='The property was updated'
    success_delete='The property was deleted'

    def get_queryset(self):
        return Property.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        raw_country=request.POST.get('country_raw')
        country_code = raw_country.split(',')[0]
        country = raw_country.split(',')[1]
        raw_data=request.POST.get('property_type_raw')
        property_type = raw_data.split(',')[0]
        property_category = raw_data.split(',')[1] 
        request.data._mutable = True
        # print("[pppppppppppppppppppppppppppppppppppppppppp]",property_type)
        # print("[rrrrrrrrrrrrrrrrrrrr]",property_category)
        request.data['property_type']=property_type
        request.data['property_category']=property_category
        request.data['country_code']=country_code
        request.data['country']=country
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': self.success_update,
                'response': serializer.data,
              
            })
        else:
            error_response =  error_loop.fix_errors(serializer.errors)
            return Response({
                
                'error': error_response
            })

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_property(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Property.objects.all()
    serializer_class = PropertySerializers
    success_insert='Your property has been added'
    def create(self, request, format=None, *args, **kwargs):
        raw_data=request.POST.get('property_type_raw')
        raw_country=request.POST.get('country_raw')
        random_value=request.POST.get('random_value')
        country_code = raw_country.split(',')[0]
        country = raw_country.split(',')[1]
        property_type = raw_data.split(',')[0]
        property_category = raw_data.split(',')[1]
        request.data._mutable = True
        request.data['property_name']=request.POST.get('property_name')
        request.data['property_type']=property_type
        request.data['property_category']=property_category
        request.data['country_code']=country_code
        request.data['country']=country
        request.data['random_value']=random_value
        # request.data['managed_by']=self.request.user.id
        # request.data['owned_by']=self.request.user.id
        # request.data['property_managed_by']=property_category
       
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            # print(serializer.data)

            saved_user2 = serializer.save(added_by=self.request.user)

            property_auto= serializer.data['id']
            property_name= request.POST.get('property_name')
         
            return Response({
                'property_auto': property_auto,
                'property_name': property_name,
               
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
        # print(self.request.user.user_type)
        data=Property.objects.all().order_by('property_name')
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'property_category','property_name', 'property_type','city','street')
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
                row.property_name,
                f'''   
                {row.property_category}
                <br>
                 {row.property_type}
                ''',
               f' {row.property_owner} ',
               f' {row.city} <br> {row.street} ',
              
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
                       
                        <a class="dropdown-item edit_property_button text-primary" id="{row.id}">Edit</a>
                        <a class="dropdown-item delete_property_button text-primary" id="{row.property_name},{row.id}">Delete</a>
                         <hr>
                        <a class="dropdown-item" href="{reverse('property:details', kwargs={'property': row.id })}">Property details (New page)</a>
                        <a class="dropdown-item" href="{reverse('property:units', kwargs={'property': row.id })}">Open units (New page)</a>

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
    

class EditDelete_units(custom_apiviews.RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    serializer_class = UnitSerializers
    queryset = Unit.objects.all()
    success_update='The unit was updated'
    success_delete='The unit was deleted'

    def get_queryset(self):
        return Unit.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_units(custom_apiviews.ListBulkCreateAPIView):
    data = []
    queryset = Unit.objects.all()
    serializer_class = UnitSerializers
    success_insert='Your units have been added'

    def create(self, request, format=None, *args, **kwargs):
     
        the_data=bulk_data_fomart_decision(request.data) 
      
        
        many = isinstance(the_data, list)
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            unit_property= serializer.data[0]['unit_property']
            saved_user2 = serializer.save(added_by=self.request.user)

            return Response({
                'unit_property': unit_property,
                'success': self.success_insert,
                # 'response': serializer.data,
            })
        else:
            error_response = error_loop.fix_errors_bulk(serializer.errors)
            return Response({
                'error': error_response
            })


    def get_queryset(self):
        added_by=self.request.user.id
        property_id=self.request.query_params.get('property_id')
        if property_id:
            data = Unit.objects.select_related('unit_property').filter(unit_property=property_id)

        else:
            data = Unit.objects.select_related('unit_property').all()
        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'unit_name', 'unit_category','occupancy_status')
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
        amount=2
        total_sum=72
        row_data = filtered_queryset[start:end]
        for row in row_data:
            occupancy_status=row.occupancy_status
            if row.occupancy_status=="personal use":
               occupancy_status="For personal use"
            data.append([
                row.unit_property.property_name,
               row.unit_name,
					
                f'''<span> {row.unit_category}<br> <span> {row.unit_type} </span><br>	
					''',
                 occupancy_status,
              
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
                        <a class="dropdown-item edit_units_button text-primary" id="{row.id}">Edit</a>
                        <a class="dropdown-item delete_units_button text-primary" id="{row.unit_name},{row.id}">Delete</a>
                         <hr>
                        <a class="dropdown-item" href="{reverse('property:unit-detail', kwargs={'unit': row.id })}">Open details (New page)</a>

                    </div>
                </div>
               ''',
            ])
        response = {
            'total_sum': total_sum,
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'aaData': data,
           
            
        }
        return Response(response)

    
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def prepare_unit(request,*args, **kwargs):
    unit_list=[]
    total_units=request.POST.get('total_units')
    raw_data=request.POST.get('property_data')
    property_auto = raw_data.split(',')[0]
    current_unit = raw_data.split(',')[1]
    unit_create_type=request.POST.get('unit_create_type')
    unit_create_name=request.POST.get('unit_create_name')
    property_data=Property.objects.get(id=property_auto)
    current_unit_number=int(current_unit)
    total_unit_number=int(total_units)
    cap=total_unit_number+current_unit_number
    
    data = []
    for item in range(current_unit_number,cap):
        if unit_create_type=="alphabets":
            x='A'
            unit_number=chr(ord(x) + item)
        else:
            unit_number=item
            
        
        data.append ([
            f''' {property_data.property_name} <span class=" fancy_text3  {property_auto}">( <span class="unit_buildings">{total_units } </span> units)</span> ''',
            f'''
            <input type="hidden" class="{property_auto}_{property_data.property_name}_units" value="{total_units}">
					<div class="col-121 unit_columns">
					<div class="form-inline justify-content-sm-start">
						<select class="form-controld form-controls unit_upload_decision" data-tab="{property_auto}_{property_data.property_name}" name="upload_decision" style="background-color:#FFFFE0;border:1px solid grey">
							<option value="upload">Upload this unit</option>
							<option value="no upload">Ignore this unit</option>
						</select>
					</div>
				</div>
            
            ''',
           
            f'''
					<input type="hidden" name="unit_property" value="{property_auto}">
					<input type="hidden" name="create_nos" value="{item}">
					<input type="hidden" name="unit_category" value="{property_data.property_category}">
		
					<div class="col-sm-121 unit_columns">
					<div class="form-group justify-content-sm-start col-12">
						<label class="control-label"> </label>
						<div class="input-group mb-2 mb-sm-0">
							<input autocomplete="off" class="form-controld editable" name="unit_name" type="text" value="{unit_create_name} {unit_number}">
						</div>
					</div>
				</div>
            
            ''',
             f'''
           
				<div class="col-121 ">
					<div class="form-inline justify-content-sm-start">
						<select class="form-controld fsorm-controls" name="occupancy_status" s1tyle="background-color:#FFFFE0;border:1px solid grey">
							<option value="vacant">Unit is for rent</option>
							<option value="not sold">For selling</option>
							<option value="personal use">For personal use</option>
						</select>
					</div>
				</div>
            
            ''',
        ])
        unit_list.append(item)
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,
            'unit_list': unit_list,
            'property_create_number': property_auto,
        }
    return Response(response)

@api_view(('GET','POST','PUT'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def unit_update(request):
    
    unit_list=request.POST.get('unit_list').split(",")
    unit_list=[int(i) for i in unit_list]
    # unit_list=[int(i) for i in unit_list]
    unit_name=request.POST.get('unit_name')
    unit_property=request.POST.get('details_based_id')
    unit_category=request.POST.get('unit_category')
    unit_type=request.POST.get('unit_type')
    size=request.POST.get('size')
    baths=request.POST.get('baths')
    is_furnished=request.POST.get('is_furnished')
    description=request.POST.get('description')
    if size=="":
        size=None
    if unit_name:
        Unit.objects.filter(create_nos__in=unit_list,unit_property=unit_property).update(unit_name=unit_name,
            unit_category=unit_category,unit_type=unit_type,size=size,baths=baths,is_furnished=is_furnished,description=description)
    else:
        Unit.objects.filter(create_nos__in=unit_list,unit_property=unit_property).update(
            unit_category=unit_category,unit_type=unit_type,size=size,baths=baths,is_furnished=is_furnished,description=description)


  
    response = {
            'success': 'Sucessfully updated the units',
          
        }
        
    return Response(response)


class EditDelete_features(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = FeaturesSerializers
    queryset = Unit_features.objects.all()
    success_update='The feature was updated'
    success_delete='The feature was deleted'

    def get_queryset(self):
        return Unit_features.objects.all()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        action=request.POST.get('action')   
        charge_id=request.POST.get('id')   
        property_create_number=request.POST.get('property_create_number')   
        id_list=request.POST.get('id_list').split(",")
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   

        if action=="update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        else:
            many=False
            serializer = self.get_serializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            if action !="update":
                new_id= serializer.data['id']
                id_list.remove(charge_id)
                id_list.append(new_id)
                unit_create_numbers=[int(i) for i in unit_create_numbers]
                data=Unit.objects.filter(create_nos__in=unit_create_numbers)
                Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
                unit_features=id_list)

                
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
        feature_id=request.POST.get('feature_id')   
        property_create_number=request.POST.get('property_create_number')   
        id_list=request.POST.get('id_list').split(",")
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",") 
        if action=="update":
            self.perform_destroy(instance)
     
        id_list.remove(feature_id)
        Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
            unit_features=id_list)
        return Response({
                'id_list': id_list,
                'success': self.success_delete,
                # 'status':status.HTTP_204_NO_CONTENT
            })

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_features(custom_apiviews.ListBulkCreateAPIView):
  
    data = []
    queryset = Unit_features.objects.all()
    serializer_class = FeaturesSerializers
    success_insert='Your feature has been added'
    def create(self, request, format=None, *args, **kwargs):
        property_create_number=request.POST.get('property_create_number') 
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   
       
        id_list=request.POST.get('id_list').split(",") 

            
            
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            # if category !="custom":
            #     saved_user2 = serializer.save(added_by=self.request.user,name=category)
            # else:
            saved_user2 = serializer.save(added_by=self.request.user)
            feature_id= serializer.data['id']
            id_list=list(filter(None, id_list))

            id_list.append(feature_id)
            Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
             unit_features=id_list)
        
         
            return Response({
                'feature_id': feature_id,
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
        data=Unit_features.objects.filter(id__in=id_list)

        return data

    def filter_for_datatable(self, queryset):
   
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name')
            ).filter()
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
                        <a class="dropdown-item edit_features_button text-primary" id="{row.id}">Edit</a>
                        <a class="dropdown-item delete_features_button text-primary" id="{row.name},{row.id},{row.created_at}">Delete</a>
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
    
class EditDelete_photos(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = PhotoSerializers
    queryset = Unit_photos.objects.all()
    success_update='The photo was updated'
    success_delete='The photo was deleted'

    def get_queryset(self):
        return Unit_photos.objects.all()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        action=request.POST.get('action')   
        charge_id=request.POST.get('id')   
        property_create_number=request.POST.get('property_create_number')   
        id_list=request.POST.get('id_list').split(",")
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   

        if action=="update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        else:
            many=False
            serializer = self.get_serializer(data=request.data, many=many)

        if serializer.is_valid():
            serializer.save()
            if action !="update":
                new_id= serializer.data['id']
                id_list.remove(charge_id)
                id_list.append(new_id)
                unit_create_numbers=[int(i) for i in unit_create_numbers]
                data=Unit.objects.filter(create_nos__in=unit_create_numbers)
                Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
                unit_photos=id_list)

                
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
        feature_id=request.POST.get('photo_id')   
        property_create_number=request.POST.get('property_create_number')   
        id_list=request.POST.get('id_list').split(",")
        print("id list",id_list)
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",") 
        if action=="update":
            self.perform_destroy(instance)
        
        id_list.remove(feature_id)
        Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
            unit_photos=id_list)
        return Response({
                'id_list': id_list,
                'success': self.success_delete,
                # 'status':status.HTTP_204_NO_CONTENT
            })



    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_photos(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Unit_photos.objects.all()
    serializer_class = PhotoSerializers
    success_insert='Your photo has been added'
    def create(self, request, format=None, *args, **kwargs):
        unit_create_numbers=request.POST.get('unit_create_numbers').split(",")   
        property_create_number=request.POST.get('property_create_number')   
       
        id_list=request.POST.get('id_list').split(",") 

            
            
        the_data=request.data
        many=False
        serializer = self.get_serializer(data=the_data, many=many)
        if serializer.is_valid():
            # if category !="custom":
            #     saved_user2 = serializer.save(added_by=self.request.user,name=category)
            # else:
            saved_user2 = serializer.save(added_by=self.request.user)
            feature_id= serializer.data['id']
            id_list=list(filter(None, id_list))

            id_list.append(feature_id)
            Unit.objects.filter(create_nos__in=unit_create_numbers,unit_property=property_create_number).update(
             unit_photos=id_list)
        
         
            return Response({
                'photo_id': feature_id,
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
        data=Unit_photos.objects.filter(id__in=id_list)
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
                f'<img src="{row.photo.url}" alt="unit photo" style="width:50px;height:50px;border:2px solid grey;">',
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
                        <a class="dropdown-item" href="{row.photo.url}" id="{row.id}" download>Download</a>
                        <a class="dropdown-item delete_photos_button" id="{row.name},{row.id},{row.created_at}">Delete</a>
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
    
class EditDelete_documents(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = DocumentSerializers
    queryset = Property_documents.objects.all()
    success_update='The document was updated'
    success_delete='The document was deleted'

    def get_queryset(self):
        return Property_documents.objects.all()
  
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_documents(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Property_documents.objects.all()
    serializer_class = DocumentSerializers
    success_insert='Your document has been added'
   

    def get_queryset(self):
        random_value=self.request.query_params.get('random_value')
    
        data=Property_documents.objects.filter(random_value=random_value)
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
           document_url=row.document.url
           data.append ([
                # f'<img src="{row.photo.url}" alt="unit photo" style="width:50px;height:50px;border:2px solid grey;">',
                f'''<span class="me-3 text-primary">
										<svg id="icon-orders" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-file-text">
											<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
											<polyline points="14 2 14 8 20 8"></polyline>
											<line x1="16" y1="13" x2="8" y2="13"></line>
											<line x1="16" y1="17" x2="8" y2="17"></line>
											<polyline points="10 9 9 9 8 9"></polyline>
										</svg>
						</span>	<span class="fancy_text5 text-primary f-16"> {row.name}	</span> ''',
                
            #    row.name,
            #    row.category,
               f'<a class="fancy_text5 btn btn-outline-primary px-4 py-1" href="{document_url}"  download="{row.name}">View {row.category}</a>',
               f'<a class=" delete_document_button btn btn-outline-danger px-4 py-2" id="{row.name},{row.id},{row.random_value}">Delete</a>',

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
                        <a class="dropdown-item" href="{row.document.url}" id="{row.id}" download>Download</a>
                        
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
def handle_past_notifications():
    print("PPPPPPPAST notification called")
    
class EditDelete_utility(custom_apiviews.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = UtilitySerializers
    queryset = Utility_bills.objects.all()
    success_update='The utility was updated'
    success_delete='The utility was deleted'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        name=request.POST.get('name')
        group_utility=request.POST.get('group')
        year_date=request.POST.get('year_date')
        month_date=request.POST.get('month_date')
        present =datetime.now()
        today=date.today()
        print("===================================")
        print(group_utility)
        # print("===================================")
        # print(year_date)

      
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

    def get_queryset(self):
        return Utility_bills.objects.all()
  
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ListCreate_utility(custom_apiviews.ListBulkCreateAPIView):

    data = []
    queryset = Utility_bills.objects.all()
    serializer_class = UtilitySerializers
    success_insert='Your utility has been added'

    def get_queryset(self):
        random_value=self.request.query_params.get('random_value')
    
        data=Utility_bills.objects.filter(random_value=random_value)
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
            if row.group=="tax":
                date=f'{row.year_date} of every year'
            else:
                date=f'{ordinal(row.month_date)} of every month'
            
            data.append ([
                row.name,
                row.category,
                date ,
               

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
                        <a class="dropdown-item fancy_text5  edit_utility_button  px-4 py-1" id="{row.id}">Click to edit</a>
                        <a class="dropdown-item delete_utility_button px-4 py-2" id="{row.name},{row.id},{row.random_value}">Click to delete</a>
                        
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
    
      

        


    

