from django.contrib import admin
from .models import Property, MaintenanceRequest, Payment

# Register your models here.
class PropertyList(admin.ModelAdmin):
    list_display = ( 'property_name', 'apt_no',)
    search_fields = ('property_name', )
    ordering = ['property_name']

class RentList(admin.ModelAdmin):
    list_display = ( 'rent',)
    search_fields = ( 'rent',)
    ordering = ['rent']

class MaintenanceRequestList(admin.ModelAdmin):
    list_display = ( 'problem', 'status')
    search_fields = ('problem', )
    ordering = ['status']

class PaymentList(admin.ModelAdmin):
    list_display = ( 'amount_paid',)
    search_fields = ( 'amount_paid',)
    ordering = ['amount_paid']

admin.site.register(Property, PropertyList)
admin.site.register(MaintenanceRequest, MaintenanceRequestList)
admin.site.register(Payment, PaymentList)
