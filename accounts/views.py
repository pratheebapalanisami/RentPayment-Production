from accounts.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from rentapp.models import Property

from .forms import UserLoginForm, CustomerRegistrationForm
from django.urls import reverse

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print("Logged in")
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            print("Logged in")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("Logged in")
                    if user.profile.is_employee or user.is_superuser:
                        return render(request, 'rentapp/home.html')
                    elif user.profile.is_tenant or user.is_superuser:
                        return HttpResponseRedirect(reverse('rentapp/home'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_tenant(request):
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user, is_tenant=True)
            #property = Property.objects.get(apt_no=user_form.cleaned_data['apt_no'])
            #Tenant.objects.create(user=new_user, apt_no=property, lease_start_date=user_form.cleaned_data['lease_start_date'], lease_end_date=user_form.cleaned_data['lease_end_date'])
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = CustomerRegistrationForm()
    return render(request,
                  'accounts/tenant/register.html',
                  {'user_form': user_form})

def register_employee(request):
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user, is_employee=True)
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = CustomerRegistrationForm()
    return render(request,
                  'accounts/employee/register.html',
                  {'user_form': user_form})

