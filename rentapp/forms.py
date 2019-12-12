
from django import forms
from .models import Payment, Property, MaintenanceRequest


class PropertyForm(forms.ModelForm):
   class Meta:
       model = Property
       fields = ('user', 'apt_no', 'property_name', 'rent_amount', 'address', 'city', 'state', 'zipcode')

class PaymentForm(forms.ModelForm):
   class Meta:
       model = Payment
       fields = ('amount_paid', 'paid_date')

class MaintenanceRequestForm(forms.ModelForm):
   class Meta:
       model = MaintenanceRequest
       fields = ('property', 'priority', 'status', 'problem', 'resolved_by')

