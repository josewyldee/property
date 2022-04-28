from rest_framework import serializers
from .models import Charges, Expense,Invoice,Receipt,Statement,Payment_options
from django.utils import timezone



class ChargeSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Charges
        exclude = ['added_by']
class InvoiceSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Invoice
        exclude = ['added_by']
    def __init__(self, *args, **kwargs):
        super(InvoiceSerializers, self).__init__(*args, **kwargs)
        self.fields['late_fee_grace'].required = False
        self.fields['late_fee_max'].required = False
class ReceiptSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))

    class Meta:
        model = Receipt
        exclude = ['added_by']
class ExpenseSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))

    class Meta:
        model = Expense
        exclude = ['added_by']
        exclude = ['added_by']
class PaymentOptionsSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))

    class Meta:
        model = Payment_options
        exclude = ['added_by']
