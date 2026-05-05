from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),

#salesperson pages
    path('branch-inventory/', views.branch_inventory_view, name='branch_inventory'),
    path('manage-customers/', views.manage_customers_view, name='manage_customers'),    
    path('record-purchase/', views.record_purchase_view, name='record_purchase'),
    path('transaction-history/', views.transaction_history_view, name='transaction_history'),
    path("api/transactions/view/", views.view_transactions, name="view_transactions"),
    path("api/transactions/add/", views.add_transaction, name="add-transaction"),
    path("api/invoice/<int:transaction_id>/", views.generate_invoice, name="generate-invoice"),

# Manager Pages
    path('products-page/', views.manage_products, name='manage-products'),
    path('inventory-page/', views.manage_inventory, name='manage-inventory'),
    path('suppliers-page/', views.manage_suppliers, name='manage-suppliers'),
    path('purchase-order-page/', views.create_purchase_order_page, name='create-purchase-order'),
    path('reports-page/', views.generate_report_page, name='generate-reports'),
    path("api/purchase-order/add/", views.create_purchase_order, name="create-purchase-order-api"),
    path("purchase-orders/", views.list_purchase_orders, name="list-purchase-orders"),
    path("purchase-order/<int:order_id>/", views.get_purchase_order, name="get-purchase-order"),
    path("purchase/update/<int:order_id>/", views.update_purchase, name="update-purchase"),
    path("api/customers/add/", views.add_customer, name="add-customer"),
    path("api/customers/update/<int:customer_id>/", views.update_customer, name="update-customer"),

    path("api/products/add/", views.add_product, name="add-product"),
    path("api/products/view/", views.view_products, name="view-products"),
    path("api/products/update/<int:product_id>/", views.update_product, name="update-product"),
    path("api/products/delete/<int:product_id>/", views.delete_product, name="delete-product"),

    path("api/inventory/view/", views.view_branch_inventory, name="view-branch-inventory"),
    path("api/inventory/update/", views.update_inventory, name="update-inventory"),

    path("api/suppliers/add/", views.add_supplier, name="add-supplier"),
    path("api/suppliers/update/<int:supplier_id>/", views.update_supplier, name="update-supplier"),
    path("api/suppliers/delete/<int:supplier_id>/", views.delete_supplier, name="delete-supplier"),
]
