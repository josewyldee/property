from datetime import datetime
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Property,Property_documents,Utility_bills,Unit
from finance.models import Charges,Expense
from datetime import date,datetime
from notifications.models import Notification
@receiver(post_save, sender=Property)
def property_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    documents = Property_documents.objects.filter(random_value=instance.random_value)
    documents.update(property=instance.id)
    utility = Utility_bills.objects.filter(random_value=instance.random_value)
    utility.update(property=instance.id)
    for row in utility:
        name=row.name
        group_utility=row.group
        year_date=row.year_date
        month_date=row.month_date
        present =datetime.now()
        today=date.today()
        if group_utility!='tax':
            print("This is Not tax")
            date_month_day=month_date
            date_month_month=today.month
            date_month_year=today.year
            print("-----------------------------------")
            print("MONTH -- day:",date_month_day ,"Month:",date_month_month,"Year:",date_month_year)
            string_month_date = f"{date_month_day}/{date_month_month}/{date_month_year}"
            cooked_month_date =datetime.strptime(string_month_date, "%d/%m/%Y")

            if cooked_month_date.date() < present.date():
                created_on=today
                expense=Expense.objects.create(amount=row.amount,property=instance,expense_name=row.name,expense_group=row.group,created_on=created_on,added_by=row.added_by)
                message=f"Attach payment document for {name} "
                title="Expense reminder"
                to_group="staff"
                to_id=None
                notification_type="expense"
                from_group="system"
                from_user=None
                foreign_instance=expense
                Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)
            else:
                print("cooked month date is greter")
            print("----------------------------------------------")
            
        else:
            print("This is tax")

            data_year= year_date
            data_year_day=data_year.split(',')[0]
            data_year_month=datetime.strptime(data_year.split(',')[1], "%B").month
            date_year_year=today.year
            print("-----------------------------------")
            print("YEAR-----day:",data_year_day ,"Month:",data_year_month,"Year:",date_year_year)
            string_year_date = f"{data_year_day}/{data_year_month}/{date_year_year}"
            cooked_year_date =datetime.strptime(string_year_date, "%d/%m/%Y")

            if cooked_year_date.date() < present.date():
                created_on=today
                expense=Expense.objects.create(amount=row.amount,property=instance,expense_name=row.name,expense_group=row.group,created_on=created_on,added_by=row.added_by)

                message=f"Attach payment document for {name} "
                title="Expense reminder"
                to_group="staff"
                to_id=None
                notification_type="expense"
                from_group="system"
                from_user=None
                foreign_instance=expense
                Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)
            else:
                print("cooked year date is greter")
            print("----------------------------------------------")


    id_list=None
    if instance.occupancy_status=="vacant" or instance.occupancy_status=="rented" :
        charges=Charges.objects.create(property=instance,name=instance.property_rent_name,category=instance.property_rent_category,amount=instance.property_rent_amount,month_date=instance.property_rent_date,duration=instance.property_rent_duration,added_by=instance.added_by)
        print(instance.property_rent_amount)
        print("90900000000000000")
        data=charges.id
        id_list=[f'{data}']
        
     
        print("iiiiiiiiiiiiiiiiiiidddlist",id_list)
    
    if created:
        unit=Unit.objects.create(description=instance.description,occupancy_status=instance.occupancy_status,unit_name=instance.property_name,unit_property=instance,unit_category=instance.property_category,unit_type=instance.property_type,added_by=instance.added_by,added_on=instance.added_on)
        if id_list: 
            unit.unit_charges=id_list
            unit.save()
    else:
        unit=Unit.objects.filter(unit_property=instance)
        if unit:
            if instance.occupancy_status=="not avaialble":
                unit.update(description=instance.description,unit_name=instance.property_name,unit_category=instance.property_category,unit_type=instance.property_type)
                if id_list:
                    unit.update(unit_charges=id_list)
                else:
                    unit.update(unit_charges=None)

            else:
                unit.update(description=instance.description,occupancy_status=instance.occupancy_status,unit_name=instance.property_name,unit_category=instance.property_category,unit_type=instance.property_type)
                if id_list:
                    unit.update(unit_charges=id_list)
                else:
                    unit.update(unit_charges=None)
        else:
            unit=Unit.objects.create(description=instance.description,occupancy_status=instance.occupancy_status,unit_name=instance.property_name,unit_property=instance,unit_category=instance.property_category,unit_type=instance.property_type,added_by=instance.added_by,added_on=instance.added_on)
            if id_list: 
                    unit.unit_charges=id_list
                    unit.save()
    
# @receiver(post_save, sender=Utility_bills)
# def property_post_save(sender,instance,created, **kwargs):
#     name=instance.name
#     group_utility=instance.group
#     year_date=instance.year_date
#     month_date=instance.month_date
#     present =datetime.now()
#     today=date.today()
#     if group_utility!='tax':
#         print("This is Not tax")
#         date_month_day=month_date
#         date_month_month=today.month
#         date_month_year=today.year
#         print("-----------------------------------")
#         print("MONTH -- day:",date_month_day ,"Month:",date_month_month,"Year:",date_month_year)
#         string_month_date = f"{date_month_day}/{date_month_month}/{date_month_year}"
#         cooked_month_date =datetime.strptime(string_month_date, "%d/%m/%Y")

#         if cooked_month_date.date() < present.date():
#             created_on=today
#             expense=Expense.objects.create(amount=instance.amount,property=instance.property,expense_name=instance.name,expense_group=instance.group,created_on=created_on,added_by=instance.added_by)
#             message=f"Attach payment document for {name} "
#             title="Expense reminder"
#             to_group="staff"
#             to_id=None
#             notification_type="expense"
#             from_group="system"
#             from_user=None
#             foreign_instance=expense
#             Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)
#         else:
#             print("cooked month date is greter")
#         print("----------------------------------------------")
           
#     else:
#         print("This is tax")

#         data_year= year_date
#         data_year_day=data_year.split(',')[0]
#         data_year_month=datetime.strptime(data_year.split(',')[1], "%B").month
#         date_year_year=today.year
#         print("-----------------------------------")
#         print("YEAR-----day:",data_year_day ,"Month:",data_year_month,"Year:",date_year_year)
#         string_year_date = f"{data_year_day}/{data_year_month}/{date_year_year}"
#         cooked_year_date =datetime.strptime(string_year_date, "%d/%m/%Y")

#         if cooked_year_date.date() < present.date():
#             created_on=today
#             expense=Expense.objects.create(amount=instance.amount,property=instance.property,expense_name=instance.name,expense_group=instance.group,created_on=created_on,added_by=instance.added_by)

#             message=f"Attach payment document for {name} "
#             title="Expense reminder"
#             to_group="staff"
#             to_id=None
#             notification_type="expense"
#             from_group="system"
#             from_user=None
#             foreign_instance=expense
#             Notification.objects.create(expense=foreign_instance,title=title,message=message,notification_type=notification_type,from_group=from_group,from_user=from_user,to_group=to_group,to_id=to_id)
#         else:
#             print("cooked year date is greter")
#         print("----------------------------------------------")