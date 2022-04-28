from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from rest_framework.response import Response
from django.shortcuts import redirect
from utils import custom_apiviews,error_loop
from .serializers import NotificationSerializer,Notification

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
def index(request):


    print("-----------------------------------------joseph disraeli omenda")
    if request.user.is_tenant:
        return redirect('/tenant_dashboard/')
    if request.user.is_syestem_admin:
        notifications=Notification.objects.all()
        notifications.update(status="read")
    return render(request, 'notifications/index.html', {})


def room(request, room_name):
    return render(request, 'notifications/chatroom.html', {
        'room_name': room_name
    })

def open(request,notification,notification_type,id):
    notif = Notification.objects.get(id=notification)
    notif.status="read"
    notif.save()
  

  
    if notification_type=="maintenance":
        id=int(id)
        return redirect('maintenance:details', maintenance=id)
    elif notification_type=="lease":
        id=int(id)
        return redirect('tenant:lease_details', id=id)

    elif notification_type=="invoice":
        return redirect('finance:invoice-document', invoice=id)
    elif notification_type=="receipt":
        return redirect('finance:receipt-document', receipt=id)
    elif notification_type=="expense":
        return redirect('finance:expenses')
    else:
        return redirect('notifications:index')
@api_view(('GET','POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def update_status(request,id):
    notif = Notification.objects.get(id=id)
    notif.status="read"
    notif.save()
    response = {
            'success': 'done'
        }
    return Response(response)
class EditDelete_notification(custom_apiviews.RetrieveUpdateDestroyAPIView):


    lookup_field = 'id'
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    success_update='The notification was updated successfully'
    success_delete='The notification was deleted successfully'

    def get_queryset(self):
        return Notification.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class ListCreate_notification(custom_apiviews.ListCreateAPIView):
    data = []
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    success_insert='The notification has been added'
    
    def get_queryset(self):
        # tenant=self.request.query_params.get('tenant')
        data = Notification.objects.select_related('from_user').all()
        return data

    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'notification_type', )
            ).filter(search__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        row_data = self.filter_for_datatable(queryset)
        data = []
        for row in row_data:
            from_user=row.from_group
            if row.maintenance:
                icon='<i class="fa fa-wrench"></i>'
                media_color="media-danger"
                link=f"href={reverse('notifications:open', kwargs={'notification': row.id,'notification_type': row.notification_type,'id': row.maintenance.id})}"
                
            elif row.statement:
                icon='<i class="fa fa-money"></i>'
                media_color="media-primary"
                link=f"href={reverse('notifications:open', kwargs={'notification': row.id,'notification_type': row.notification_type,'id': row.statement.statement_invoice})}"
                
            elif row.lease:
                icon='<i class="fa fa-home"></i>'
                media_color="media-success"
                link=f"href={reverse('notifications:open', kwargs={'notification': row.id,'notification_type': row.notification_type,'id': row.lease.id})}"
            elif row.expense:
                icon='<i class="fa fa-money"></i>'
                media_color="media-danger"
                link=f"href={reverse('notifications:open', kwargs={'notification': row.id,'notification_type': row.notification_type,'id': row.expense.id})}"
            else:
                icon='<i class="fa fa-home"></i>'
                media_color="media-success"
                link=f"href={reverse('notifications:open', kwargs={'notification': row.id,'notification_type': row.notification_type,'id': 7})}"
            if row.from_user:
                from_user=f'@{row.from_user.username}'
              
            data.append([
               
                f'''
                <div class="widget-media">
                <ul class="timeline">
				<li>
					<div class="timeline-panel">
						<div class="media mr-2 btn-rounded {media_color} ">
							{icon}
						</div>
						<a {link} >
							<div class="media-body">
								<h6 class="mb-1"> {row.title} </h6>
                          
                                <small>{row.message}</small>
								
							</div>
						</a> 
					</div>
				</li>
			</ul></div>
                ''',
                   f'''          
                 {row.since} days ago
                  ''',
                  from_user,
                  row.status,
                  f'<button class="btn btn-primary light btn-rounded px-4 py-1 view_notification" id="{row.id}">View </button>'
                
                
            ])
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': row_data.count(),
            'aaData': data
        }
        return Response(response)


