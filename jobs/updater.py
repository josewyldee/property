from datetime import datetime
import imp
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import create_auto_invoice,send_auto_lease_notification,create_auto_late_fee,send_auto_expense,send_expense_reminder
# from finance.views import create_auto_invoice

def start():
	# scheduler = BackgroundScheduler()
    scheduler = BackgroundScheduler(timezone="Africa/Nairobi")
    scheduler.add_job(create_auto_invoice, 'cron', hour=1, minute=10)
    scheduler.add_job(send_auto_lease_notification, 'cron', hour=1, minute=7)
    scheduler.add_job(create_auto_late_fee, 'cron', hour=1, minute=4)
    scheduler.add_job(send_auto_expense, 'cron', hour=1, minute=1)
    scheduler.add_job(send_expense_reminder, 'cron', hour=23, minute=50)
    # scheduler.add_job(schedule_api, 'interval', seconds=4)
    scheduler.start()