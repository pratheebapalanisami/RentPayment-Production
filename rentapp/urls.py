from accounts.views import user_login
from django.urls import path, re_path
from rentapp.views import home
from django.conf.urls import url

from . import views

app_name = 'rentpayment'

urlpatterns = [
    path('',user_login, name='login'),
    re_path(r'^home/$', home, name='home'),
    path('employee/property_list', views.property_list, name='property_list'),
    path('employee/add_property', views.add_property, name='add_property'),
    path('employee/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('employee/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('employee/maintenance_request_list', views.maintenance_request_list, name='maintenance_request_list'),
    path('employee/<int:pk>/maintenance_request_update', views.maintenance_request_update, name='maintenance_request_update'),
    path('tenant/pay_rent', views.pay_rent, name='pay_rent'),
    path('tenant/payment_detail', views.payment_detail, name='payment_detail'),
    path('tenant/payment_success', views.payment_success, name='payment_success'),
    path('tenant/payment_history', views.payment_history, name='payment_history'),
    path('tenant/maintenance_request', views.maintenance_request, name='maintenance_request'),
    path('tenant/maintenance_request_history', views.maintenance_request_history, name='maintenance_request_history'),
]
