from rest_framework import serializers
from .models import Property, MaintenanceRequest, Payment


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('user', 'apt_no', 'property_name', 'rent_amount', 'address', 'city', 'state', 'zipcode')

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = ('property', 'priority', 'status', 'problem', 'resolved_by')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('amount_paid', 'paid_date')