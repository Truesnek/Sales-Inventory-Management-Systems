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
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),
    path('manager/manage-products/', views.manage_products, name='manage-products'),
    path("api/customers/add/", views.add_customer, name="add-customer"),
    path("api/customers/update/<int:customer_id>/", views.update_customer, name="update-customer"),

    path("api/products/add/", views.add_product, name="add-product"),
    path("api/products/view/", views.view_products, name="view-products"),
    path("api/products/update/<int:product_id>/", views.update_product, name="update-product"),
    path("api/products/delete/<int:product_id>/", views.delete_product, name="delete-product"),

    path("api/inventory/view/", views.view_branch_inventory, name="view-branch-inventory"),
    path("api/inventory/monitor/", views.monitor_stock_levels, name="monitor-stock-levels"),
    path("api/inventory/update/", views.update_inventory, name="update-inventory"),

    path("api/suppliers/add/", views.add_supplier, name="add-supplier"),
    path("api/suppliers/update/<int:supplier_id>/", views.update_supplier, name="update-supplier"),
    path("api/suppliers/delete/<int:supplier_id>/", views.delete_supplier, name="delete-supplier"),
]
