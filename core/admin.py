from django.contrib import admin
from .models import (
    Customer, Product, Transaction, TransactionLine,
    Supplier, Branch, Carrier, Users,
    Shipment, PurchaseOrder, CustomerPurchase,
    Manager, Salesperson, Shipper,
    HasInventoryOf, IsPaidBy, TransportedIn,
    Creates, Tracks, Sells,
    GivesProductsTo, MakesPaymentTo, ReceivesProductsFrom
)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionLine)
admin.site.register(Supplier)
admin.site.register(Branch)
admin.site.register(Carrier)
admin.site.register(Users)
admin.site.register(Shipment)
admin.site.register(PurchaseOrder)
admin.site.register(CustomerPurchase)
admin.site.register(Manager)
admin.site.register(Salesperson)
admin.site.register(Shipper)
admin.site.register(HasInventoryOf)
admin.site.register(IsPaidBy)
admin.site.register(TransportedIn)
admin.site.register(Creates)
admin.site.register(Tracks)
admin.site.register(Sells)
admin.site.register(GivesProductsTo)
admin.site.register(MakesPaymentTo)
admin.site.register(ReceivesProductsFrom)