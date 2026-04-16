"""
URL configuration for sales_inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # -------------------------
    # Admin + basic pages
    # -------------------------
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('manager/manage-products/', views.manage_products, name='manage-products'),
    path('manager/manage-inventory/', views.manage_inventory, name='manage-inventory'),
    path('manager/manage-suppliers/', views.manage_suppliers, name='manage-suppliers'),
    path('manager/create-purchase-order/', views.create_purchase_order_page, name='create-purchase-order'),
    path('manager/generate-report/', views.generate_report_page, name='generate-report'),
    path('manager/manage-customers/', views.manage_customers, name='manage-customers'),
    path('manager/manage-transactions/', views.manage_transactions, name='manage-transactions'),
    path('manager/manage-shipments/', views.manage_shipments, name='manage-shipments'),
    
]