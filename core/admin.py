from django.contrib import admin
from .models import (
    Branch,
    Customer,
    Products,
    Supplier,
    Carrier,
    Users,
    Manager,
    Salesperson,
    Transactions,
    TransactionLine,
    BranchInventory,
    Shipment,
    PurchaseOrder,
    ReceivesProductsFrom,
)

admin.site.register(Branch)
admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Supplier)
admin.site.register(Carrier)
admin.site.register(Users)
admin.site.register(Manager)
admin.site.register(Salesperson)
admin.site.register(Transactions)
admin.site.register(TransactionLine)
admin.site.register(BranchInventory)
admin.site.register(Shipment)
admin.site.register(PurchaseOrder)
admin.site.register(ReceivesProductsFrom)