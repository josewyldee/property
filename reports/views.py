from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db.models import Sum,OuterRef, Subquery,Count,F,Q
from django.db.models.functions import Coalesce
from finance.models import Expense,Invoice, Receipt
from maintenance.models import Maintenance,Cost
from property.models import Property,Unit
# Create your views here.
class income_summary(TemplateView):
    
    template_name = "reports/income_summary.html"

class statements(TemplateView):
    
    template_name = "reports/statements.html"
class occupancy(TemplateView):
    
    template_name = "reports/occupancy.html"



@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def income_summary_table(request,*args, **kwargs):
       
    # Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
    # query_income=Expense.objects.values('expense_name').annotate(total_amount=Sum('amount'))
    query_expense=Expense.objects.values('expense_name').annotate(total_amount=Sum('amount'))
    prepayment=Receipt.objects.filter(is_prepayment=True,is_cancelled=False).aggregate(total_payment=Sum('amount'))
    query_income=Invoice.objects.filter(is_cancelled=False,invoice_type="invoice").values('name').annotate(total_amount=Sum('amount_sorted'))
    # query_income=Invoice.objects.filter(lease__id=lease,invoice_type="invoice").order_by('created_on')

    print("9999999999999999999999999")
    print(query_expense)
    # query_data=Statement.objects.all().select_related('lease__unit','lease__tenant','lease__unit__unit_property','lease')
    data = []

    for row in query_income:
        
        if row['total_amount'] >0:
            data.append ([
            "<span class='fancy_text5 display-7 '>Income</span>",
                row['name'],
                row['total_amount'],
                row['total_amount'],    
                0,
                
            ])
    data.append ([
      "<span class='fancy_text5 display-7 '>Income</span>",
                'Prepayments',
                prepayment['total_payment'],
                prepayment['total_payment'],    
                0,
                
    ])
    for row in query_expense:
        print(row['expense_name'])
        
        data.append ([
           "<span class='fancy_text5 display-7 '>Expenses</span>",
            row['expense_name'],
            row['total_amount'],
            0,
            row['total_amount'],    
            
        ])
 
       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,

         
        }
    return Response(response)
 
class maintenance_summary(TemplateView):
    
    template_name = "reports/maintenance_summary.html"

 
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def maintenance_summary_table(request,*args, **kwargs):
    subquery_solved = Maintenance.objects.filter(
     name=OuterRef('name'),status='solved'
    ).values('name').annotate(
      
        total_solved =  Coalesce( Count('id'), 0)
    ).values('total_solved')[:1]

    subquery_notsolved = Maintenance.objects.exclude(status="solved").filter(
     name=OuterRef('name')
    ).values('name').annotate(
        total_solved =  Coalesce( Count('id'), 0)
    ).values('total_solved')[:1]

    subquery_total = Maintenance.objects.filter(
     name=OuterRef('name')
    ).values('name').annotate(
        total_count = Coalesce( Count('id'), 0)
    ).values('total_count')[:1]
    subquery_spent = Cost.objects.filter(
     maintenance__name=OuterRef('name'),paid='paid'
    ).values('maintenance__name').annotate(
        total_spent = Coalesce( Sum('cost_total'), 0)
    ).values('total_spent')[:1]

    print("++++++++++++++++++++++++++")
    # print("solved "+subquery_solved)
    # print("total ",subquery_total)
    # print("spent ",subquery_spent)

    query = Maintenance.objects.annotate(
        total_notsolved=Coalesce(Subquery(subquery_notsolved),0),total_solved=Coalesce(Subquery(subquery_solved),0),total_count=Coalesce(Subquery(subquery_total),0),total_spent=Coalesce(Subquery(subquery_spent),0)
    ).order_by().distinct('name')
   
    data = []

    for row in query:
        total_not_solved=row.total_notsolved 
       
        data.append ([
        # f"<span class='fancy_text4 display-7 '>{row.name} </span>",
            row.name,
           
            row.total_count,
            row.total_solved,
            total_not_solved,
            row.total_spent,
            
            
        ])
    

       
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'aaData': data,

         
        }
    return Response(response)
 
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def occupancy_table(request,*args, **kwargs):

    # subquery_solved = Maintenance.objects.filter(
    #  name=OuterRef('name'),status='solved'
    # ).values('name').annotate(
    #     total_solved =  Count('id')
    # ).values('total_solved')[:1]
    # subquery_notsolved = Maintenance.objects.exclude(status="solved").filter(
    #  name=OuterRef('name')
    # ).values('name').annotate(
      
    #     total_solved =  Count('id')
    # ).values('total_solved')[:1]
    # subquery_total = Maintenance.objects.filter(
    #  name=OuterRef('name')
    # ).values('name').annotate(
    #     total_count = Count('id')
    # ).values('total_count')[:1]
    # subquery_spent = Cost.objects.filter(
    #  maintenance__name=OuterRef('name'),paid='paid'
    # ).values('maintenance__name').annotate(
    #     total_spent = Sum('cost_total')
    # ).values('total_spent')[:1]

    print("++++++++++++++++++++++++++")
    # print("solved "+subquery_solved)
    # print("total ",subquery_total)
    # print("spent ",subquery_spent)
    # query=Property.objects.all().order_by('property_name').annotate(total_vacant=Count("unit", filter=Q(unit__occupancy_status="vacant")),total_occupied=Count("unit", filter=Q(unit__occupancy_status="occupied")),total_sold=Count("unit", filter=Q(unit__occupancy_status="sold")),total_not_sold=Count("unit", filter=Q(unit__occupancy_status="not sold")),total_personal=Count("unit", filter=Q(unit__occupancy_status="personal use")),total_units=Count("unit"))
    query=Unit.objects.all().select_related('unit_property').order_by('unit_name')
    # query = Maintenance.objects.annotate(
    #     total_notsolved=Coalesce(Subquery(subquery_notsolved),0),total_solved=Coalesce(Subquery(subquery_solved),0),total_count=Coalesce(Subquery(subquery_total),0),total_spent=Coalesce(Subquery(subquery_spent),0)
    # ).order_by().distinct('name')
    # print(query.query)
    data = []
    i=1
    total_units=0
    total_occupied=0
    total_vacant=0
    total_sold=0
    total_not_sold=0
    total_personal=0
    for row in query:  
        total_units+=1    
        # print("********************")
        # print(row.unit_set.unit_name())
        if row.occupancy_status=="vacant":
            status="Vacant"
            total_vacant+=1
        if row.occupancy_status=="occupied":
            total_occupied+=1
            status="Rented"
        if row.occupancy_status=="sold":
            status="Sold"
            total_sold+=1
        if row.occupancy_status=="not sold":
            status="Not sold"
            total_not_sold+=1
        if row.occupancy_status=="personal use":
            status="Personal use"
            total_personal+=1
        data.append ([
           f'  <div class="fs-14 fancy_text5"> {i}. </div>  '  , 
            row.unit_name,
            row.unit_property.property_category,
            row.unit_property.property_type,
            row.unit_property.property_owner,
           

            status,         
     
        ])
       
    
        i+=1
        

    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),

            'total_units': total_units,
            'total_occupied': total_occupied,
            'total_vacant': total_vacant,
            'total_sold': total_sold,
            'total_not_sold': total_not_sold,
            'total_personal': total_personal,
            'aaData': data,
        }
    return Response(response)



class percentage_earnings(TemplateView):
    
    template_name = "reports/percentage_earnings.html"

 
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def percentage_earnings_table(request,*args, **kwargs):
    # query_expense=Expense.objects.values('expense_name').annotate(total_amount=Sum('amount'))
    # query_income=Invoice.objects.values('name').annotate(total_amount=Sum('amount_sorted'), filter=Q(is_cancelled=False)).filter(is_cancelled=False)

    
    subquery_income = Invoice.objects.filter(
     lease__unit__unit_property=OuterRef('id'),is_cancelled=False
    ).values('lease__unit__unit_property').annotate(
        total_income = Sum('amount_sorted')
    ).values('total_income')[:1]

    subquery_expense = Expense.objects.filter(
     property=OuterRef('id')
    ).values('property').annotate(
        total_expense = Sum('amount')
    ).values('total_expense')[:1]
    print("++++++++++++++++++++++++++")
    query = Property.objects.annotate(
        total_income=Coalesce(Subquery(subquery_income),0),total_expense=Coalesce(Subquery(subquery_expense),0)
    ).order_by().distinct('id')
    data = []
    total_income=0
    total_expense=0
    total_percent=0
    for row in query:
        percentage_earning=0
        if row.total_income > 0 or row.total_expense > 0 :
            earnings=row.total_income+row.total_expense
            percentage_earning=(row.total_income/earnings)*100
            percentage_earning=format(percentage_earning, ".2f")
            total_income+=row.total_income
            total_expense+=row.total_expense
            # percentage_earning=(earnings/row.total_expense)*100
        data.append ([
            row.property_name,
            row.property_name,
            row.total_income,
            row.total_expense,
           f'{percentage_earning} %',
        ])
    earnings=total_income+total_expense
    total_percent=(total_income/earnings)*100
    total_percent=format(total_percent, ".2f")     
    response = {
            'draw': data,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'total_income':total_income,
            'total_expense':total_expense,
            'total_percent':total_percent,
            'aaData': data,
        }
    return Response(response)