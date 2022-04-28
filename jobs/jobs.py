from finance.models import Invoice,Statement,Charges,Expense
from finance.utils import generate_transaction_id
from communications.utils import Util
from communications.models import Email
from tenant.models import Lease
from property.models import Unit
from django.conf import settings
import datetime,uuid
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.urls import reverse
from django.db.models import Q,F
from notifications.models import Notification
def send_auto_invoice_emails():
   
    email_data=[]
    statement=str(uuid.uuid4()).replace("-","").upper()
    current_site=settings.SITE_URL
   
    data=Invoice.objects.filter(communication="to be sent",created_by="system").select_related("invoice_group","lease","lease__unit","lease__tenant").distinct('invoice_group__id')
    for row in data:
        print(row.lease.tenant.name," ---",row.name,"----",row.invoice_group.id)
        from_email=row.added_by.email
        lease=row.lease
        lease_id=row.lease.id
        email=row.lease.tenant.email
        name=row.lease.tenant.name
        type_id=row.invoice_group.id
        total_amount=row.invoice_group.amount
        invoice_id=row.invoice_group.statement_invoice
        subject="Invoice"

        lease_id = urlsafe_base64_encode(smart_bytes(lease_id))
        invoice_id = urlsafe_base64_encode(smart_bytes(invoice_id))
        
        relativeLink = reverse(
                    'tenant_dashboard:invoice-pdf', kwargs={'lease': lease_id,'statement':statement,'invoice': invoice_id})
        current_site =  current_site
        absurl =settings.SITE_PROTOCOL+current_site+relativeLink
        success=0
        fail=0
        property_name=row.lease.unit.unit_property.property_name
        lease_info=f'{row.lease.unit.unit_name} {property_name}'
        if email:
            status='sent'
            reason=None

            body=f'Hope you are well. You are getting this invoice because you are a tenant of {lease_info}'
            template='email_templates/finance.html'
            email_data.append({'subject':"Invoice", 'to':email,'from':from_email,
                    'name':name,'property':property_name,'body':body,'color':'#4b72fa','template':template,'amount':total_amount,'document':None,'href':absurl })
        
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
        ,reason=reason,added_by=row.added_by
        
        )
        invoice=Invoice.objects.filter(invoice_group=row.invoice_group)
        invoice.update(communication=status)

        message=f"USD {total_amount} has been created for {name} in {lease_info}"
        title="Invoice generated"
        to_group="staff"
        to_id=None
        notification_type="invoice"
        from_group="system"
        from_user=None
        foreign_instance=row.invoice_group
        Notification.objects.create(statement=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)



    

def create_auto_late_fee():
    print("staaaaaaaaaaaaarted croooooon")
    
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


        deadline='no'
        deadline_date=None
        notify="to be sent"
        
        instance=Statement.objects.create(statement_invoice=invoice_group,lease=lease,type='invoice',amount=amount,created_on=today,added_by=row.added_by)
     
 
        
        Invoice.objects.create(added_on=today
        ,lease=lease
        ,invoice_group=instance,invoice_group_bulk=invoice_group_bulk
        ,name=name
        ,amount=amount,communication=notify
        ,deadline=deadline
        ,deadline_date=deadline_date
        ,late_fee_type=None
        ,created_on=today,added_by=row.added_by,created_by="system"
        )
       
       
        row.late_fee_status=late_fee_status
        row.amount_late_fee=overall_late_fee
        row.save()
      
        print("AUTOMATIC -----------------------------------------------------------------------------------------------------")
        print("lATE NAME name",row.late_fee_type,"Amount",row.late_fee_amount,"Deadline date:",row.deadline_date)


        print(row.id,"invoice name",row.name,"Amount charged",amount,"amount:",row.amount,"sorted:",row.amount_sorted,"new status",late_fee_status,"late fee amont",overall_late_fee)
        print("-----------------------------------------------------------------------------------------------------")
    

 
    return send_auto_invoice_emails()
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
    
    print("invoice group bulk:",invoice_group_bulk)
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

def send_auto_lease_notification():
    from datetime import datetime,timedelta
    query = Lease.objects.filter(end_lease_notice="not sent",lease_type="fixed period",active=True,end_date__gte=datetime.today(),end_date__lte=datetime.today()+timedelta(days=45)).select_related("tenant","unit","unit__unit_property")
    for row in query:
        message=f" The lease from {row.tenant.name} in {row.unit.unit_name}, {row.unit.unit_property.property_name} will expire in 45 days or less"
        title="Expiring lease"
        to_group="staff"
        to_id=None
        notification_type="lease"
        from_group="system"
        from_user=None
        foreign_instance=row
        Notification.objects.create(lease=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)

        print(message)
    query.update(end_lease_notice="sent")
def send_auto_expense():
    from property.models import Utility_bills,Property
    from notifications.models import Notification
    today=datetime.date.today()
    day_month=today.day
    created_on=today
    day_year=f'{today.day},{today.strftime("%B")}' 
    utility=Utility_bills.objects.filter(Q(month_date=day_month)|Q(year_date=day_year,group='tax') )
    for row in utility:
        if row.property:
            property=row.property
        else:
            property=Property.objects.get(random_value=row.random_value)
        print("--------",row.name)
        expense=Expense.objects.create(property=property,expense_name=row.name,expense_group=row.group,created_on=created_on,added_by=row.added_by)
        
        message=f"Expense for {row.name} is due"
        title="Expense due"
        to_group="staff"
        to_id=None
        notification_type="expense"
        from_group="system"
        from_user=None
        foreign_instance=expense
        Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)
def send_expense_reminder():
    expense=Expense.objects.filter(status="not paid")
    for row in expense:
        print("naaame",row.expense_name,"staus",row.status)
        message=f"Attach payment document for {row.name} "
        title="Expense reminder"
        to_group="staff"
        to_id=None
        notification_type="expense"
        from_group="system"
        from_user=None
        foreign_instance=expense
        Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)

