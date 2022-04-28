from django.urls import path
from . import views
app_name = "finance"


urlpatterns = [
    path('payments/', views.receipt.as_view(), name="payments"),
    path('payment_options/', views.payment_options.as_view(), name="payment_options"),
    path('payment_option-listcreate/', views.ListCreate_payment_option.as_view(), name='payment_option-listcreate'),
    path('payment_option-rud/<int:id>/', views.EditDelete_payment_option.as_view(), name='payment_option-rud'),
    path('unapplied_invoices/', views.unapplied_invoices, name="unapplied-invoices"),
    path('match_invoice/', views.match_invoice, name="match_invoice"),
    path('submit_prepayment/', views.submit_prepayment, name='submit_prepayment'),
    path('finance_history/', views.finance_history, name="finance_history"),
    path('payments-listcreate/', views.ListCreate_payments.as_view(), name='payments-listcreate'),
    path('receipt-details/', views.receipt_details, name='receipt-details'),
    path('payments-rud/<int:id>/', views.EditDelete_payments.as_view(), name='payments-rud'),
    path('receipt-document/<str:receipt>/', views.receipt_document.as_view(), name='receipt-document'),
    path('receipt-pdf/<str:receipt>/', views.receipt_pdf.as_view(), name='receipt-pdf'),

    path('debitnote/', views.debitnote.as_view(), name="debitnote"),
    path('debitnote-listcreate/', views.ListCreate_debitnote.as_view(), name='debitnote-listcreate'),
    # ----------------------------------------------------------------------------
    path('expenses/', views.expenses.as_view(), name="expenses"),
    path('expense_payments/', views.expense_payments.as_view(), name="expense_payments"),
    path('expense-listcreate/', views.ListCreate_expense.as_view(), name='expense-listcreate'),
    path('expense-rud/<int:id>/', views.EditDelete_expense.as_view(), name='expense-rud'),
 # ----------------------------------------------------------------------------
    path('payee/', views.payee.as_view(), name="payee"),
    path('payee-listcreate/', views.ListCreate_payee.as_view(), name='payee-listcreate'),
    path('payee-rud/<int:id>/', views.EditDelete_payee.as_view(), name='payee-rud'),
    # ----------------------------------------------------------------------------
   
    path('invoice/', views.invoice.as_view(), name="invoice"),
    path('invoice-listcreate/', views.ListCreate_invoice.as_view(), name='invoice-listcreate'),
    path('invoice-rud/<int:id>/', views.EditDelete_invoice.as_view(), name='invoice-rud'),
    path('invoice-details/', views.invoice_details, name='invoice-details'),
    path('invoice-document/<str:invoice>/', views.invoice_document.as_view(), name='invoice-document'),
    path('invoice-pdf/<str:invoice>', views.invoice_pdf.as_view(), name='invoice-pdf'),
    path('payments-made/', views.payments_made, name='payments-made'),

    path('creditnote/', views.creditnote.as_view(), name="creditnote"),
    path('creditnote-listcreate/', views.ListCreate_creditnote.as_view(), name='creditnote-listcreate'),
  
    # ----------------------------------------------------------------------------
   
    path('balances/', views.balances.as_view(), name="balances"),
    path('balances-listcreate/', views.balances_table.as_view(), name='balances-listcreate'),
    # ----------------------------------------------------------------------------
    path('charges-listcreate/', views.ListCreate_charges.as_view(), name='charges-listcreate'),
    path('charges-rud/<int:id>/', views.EditDelete_charges.as_view(), name='charges-rud'),

    path('test/',views.test,name="test"),
    path('test2/',views.test2,name="test2"),
    # path('test_reverse/<lease>/<invoice>',views.test_reverse,name="test_reverse"),

  
   

]
