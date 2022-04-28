from django import template
from notifications.models import Notification

register = template.Library()

@register.inclusion_tag('notifications/show_notifications.html', takes_context=True)
def show_notifications(context):
	id_list = context['request'].user.notifications
	if id_list:
		id_list = context['request'].user.notifications
	else:
		id_list=[]
	# data=Unit_features.objects.filter(id__in=id_list)
	notifications = Notification.objects.filter(id__in=id_list).exclude(status="read").order_by('-date')
	return {'notifications': notifications}


@register.simple_tag
def setvar(val=None):
  return val