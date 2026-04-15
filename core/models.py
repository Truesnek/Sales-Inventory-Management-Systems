from django.db import models

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.FloatField()
#     stock = models.IntegerField()

#     def __str__(self):
#         return self.name
    
# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)

# def __str__(self):
#         return self.name

# =========================
# CORE TABLES
# =========================

class Transaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    transaction_status = models.CharField(max_length=10)
    total_amount = models.FloatField()
    transaction_date = models.DateField()
    transaction_due_date = models.DateField()
    transaction_discount = models.FloatField()


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    contact_info = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    unit_price = models.FloatField()


class Supplier(models.Model):
    supplier_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=50)


class Branch(models.Model):
    branch_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=50)


class Shipment(models.Model):
    shipment_id = models.IntegerField(primary_key=True)
    shipment_date = models.DateField()
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    shipment_status = models.CharField(max_length=10)

    transaction = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class User(models.Model):
    employee_num = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Manager(models.Model):
    employee_num = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Salesperson(models.Model):
    employee_num = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Carrier(models.Model):
    vehicle_id = models.IntegerField(primary_key=True)
    carrier_type = models.CharField(max_length=50)
    tracking_number = models.IntegerField()


# =========================
# TRANSACTIONS
# =========================

class TransactionLine(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    line_number = models.IntegerField()
    quantity = models.IntegerField()
    unit_price_at_sale = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['transaction', 'line_number'],
                name='pk_transaction_line'
            )
        ]


class CustomerPurchase(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    sales_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['transaction', 'sales_id'],
                name='pk_customer_purchase'
            )
        ]


class PurchaseOrder(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    order_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['transaction', 'order_id'],
                name='pk_purchase_order'
            )
        ]


# =========================
# INVENTORY & RELATIONS
# =========================

class HasInventoryOf(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num_products = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'product'],
                name='pk_has_inventory_of'
            )
        ]


class TransportedIn(models.Model):
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['shipment', 'vehicle'],
                name='pk_transported_in'
            )
        ]


class Creates(models.Model):
    employee_num = models.ForeignKey(Manager, on_delete=models.CASCADE)
    transaction = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee_num', 'transaction', 'order_id'],
                name='pk_creates'
            )
        ]


class IsPaidBy(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'customer'],
                name='pk_is_paid_by'
            )
        ]


class GivesProductsTo(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    transaction = models.ForeignKey(CustomerPurchase, on_delete=models.CASCADE)
    sales_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'transaction', 'sales_id'],
                name='pk_gives_products_to'
            )
        ]


class Sells(models.Model):
    employee_num = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    transaction = models.ForeignKey(CustomerPurchase, on_delete=models.CASCADE)
    sales_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee_num', 'transaction', 'sales_id'],
                name='pk_sells'
            )
        ]


class MakesPaymentTo(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'supplier'],
                name='pk_makes_payment_to'
            )
        ]


class ReceivesProductsFrom(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    transaction = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'transaction', 'order_id', 'supplier'],
                name='pk_receives_products_from'
            )
        ]

    
