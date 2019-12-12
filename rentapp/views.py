# Create your views here.
from accounts.models import Profile, CustomUser
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from rent import settings
from rentapp.decorators import employee_required, tenant_required
from rentapp.forms import PropertyForm, MaintenanceRequestForm, PaymentForm
from rentapp.models import Property, Payment, MaintenanceRequest
from django.shortcuts import render, redirect, get_object_or_404
from rentapp.serializers import PropertySerializer, MaintenanceRequestSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


@login_required
def home(request):
    return render(request, 'rentapp/home.html')

@login_required
@employee_required
def property_list(request):
    property = Property.objects.filter()
    return render(request, 'rentapp/employee/property_list.html',
                  {'property': property})

@login_required
@employee_required
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.created_date = timezone.now()
            property.save()
            property = Property.objects.filter()
            return render(request, 'rentapp/employee/property_list.html',
                          {'property': property})
    else:
        form = PropertyForm()
        userids = Profile.objects.filter(is_tenant=True).values("user_id")
        form.fields["user"].queryset = CustomUser.objects.filter(id__in=userids)
    # print("Else")
    return render(request, 'rentapp/employee/add_property.html', {'form': form})

@login_required
@employee_required
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        # update
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            property = form.save(commit=False)
            property.updated_date = timezone.now()
            property.save()
            property = Property.objects.filter()
            return render(request, 'rentapp/employee/property_list.html',
                          {'property': property})
    else:
        # edit
        form = PropertyForm(instance=property)
    return render(request, 'rentapp/employee/property_edit.html', {'form': form})

@login_required
@employee_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return redirect('rentpayment:property_list')

@login_required
@tenant_required
def pay_rent(request):
    property = Property.objects.filter(user=request.user).first()
    is_rent_paid = _is_rent_paid(request)
    return render(request, 'rentapp/tenant/pay_rent.html', {'property': property, 'currentuser':request.user, 'is_rent_paid':is_rent_paid})

def _is_rent_paid(request):
    payment = Payment.objects.filter(user=request.user, paid_date__month=timezone.now().month)
    if len(payment) == 0:
        return False
    else:
        return True

@login_required
@tenant_required
def payment_detail(request):
    property = Property.objects.filter(user=request.user).first()
    is_rent_paid = _is_rent_paid(request)
    return render(request, 'rentapp/tenant/payment_detail.html', {'property': property, 'currentuser':request.user, 'is_rent_paid':is_rent_paid})

@login_required
@tenant_required
def payment_success(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        payment = Payment.objects.create(user=request.user, paid_date=timezone.now(),amount_paid=request.POST.get('rentamount'), property= Property.objects.filter(user=request.user).first())
        payment.save()
        return render(request, 'rentapp/tenant/payment_success.html')
    else:
        form = PaymentForm()
        # print("Else")
    return render(request, 'rentapp/tenant/payment_detail.html', {'currentuser':request.user})

@login_required
@tenant_required
def payment_history(request):
    payment = Payment.objects.filter(user=request.user)
    print(payment)
    return render(request, 'rentapp/tenant/payment_history.html', {'payment':payment})

@login_required
@tenant_required
def maintenance_request(request):
    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            print(request.POST)
            maintenancerequest = form.save(commit=False)
            maintenancerequest.created_date = timezone.now()
            maintenancerequest.user = request.user
            maintenancerequest.save()
            maintenancerequest = MaintenanceRequest.objects.filter()
            return render(request, 'rentapp/tenant/maintenance_request_history.html', {'maintenancerequest':maintenancerequest, 'currentuser':request.user})
    else:
        form = MaintenanceRequestForm()
        form.fields["property"].queryset = Property.objects.filter(user_id=request.user)
        form.fields["status"].widget.attrs['readonly'] = True
        form.fields["resolved_by"].widget= forms.HiddenInput()
        # print("Else")
    return render(request, 'rentapp/tenant/maintenance_request.html', {'form': form, 'currentuser':request.user})

@login_required
@tenant_required
def maintenance_request_history(request):
    maintenancerequest = MaintenanceRequest.objects.filter()
    return render(request, 'rentapp/tenant/maintenance_request_history.html', {'maintenancerequest': maintenancerequest, 'currentuser':request.user})

@login_required
@employee_required
def maintenance_request_list(request):
    maintenancerequest = MaintenanceRequest.objects.filter()
    return render(request, 'rentapp/employee/maintenance_request_list.html', {'maintenancerequest': maintenancerequest})

@login_required
@employee_required
def maintenance_request_update(request, pk):
    maintenancerequest = get_object_or_404(MaintenanceRequest, pk=pk)
    if request.method == "POST":
        # update
        form = MaintenanceRequestForm(request.POST, instance=maintenancerequest)
        if form.is_valid():
            maintenancerequest = form.save(commit=False)
            maintenancerequest.updated_date = timezone.now()
            maintenancerequest.save()
            maintenancerequest = MaintenanceRequest.objects.filter()
            return render(request, 'rentapp/employee/maintenance_request_list.html',
                          {'maintenancerequest': maintenancerequest})
    else:
        # edit
        maintenancerequest.resolved_by = request.user
        form = MaintenanceRequestForm(instance=maintenancerequest)

    return render(request, 'rentapp/employee/maintenance_request_update.html', {'form': form})



#API
class PropertyList(APIView):
    def get(self,request):
        properties_json = Property.objects.all()
        serializer = PropertySerializer(properties_json, many=True)
        return Response(serializer.data)

class MaintenanceRequestList(APIView):
    def get(self,request):
        maintenancerequest_json = MaintenanceRequest.objects.all()
        serializer = MaintenanceRequestSerializer(maintenancerequest_json, many=True)
        return Response(serializer.data)

class PaymentList(APIView):
    def get(self,request):
        payment_json = Payment.objects.all()
        serializer = PaymentSerializer(payment_json, many=True)
        return Response(serializer.data)
