from django.db import models

# ---------------- CORE ENTITIES ----------------

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Branch'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    num_products = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products'


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Supplier'


class Carrier(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    carrier_type = models.CharField(max_length=50, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Carrier'


# ---------------- USERS ----------------

class Users(models.Model):
    employee_number = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Users'


class Manager(models.Model):
    employee_number = models.OneToOneField(Users, on_delete=models.DO_NOTHING, primary_key=True, db_column='employee_number')
    approval_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Manager'


class Salesperson(models.Model):
    employee_number = models.OneToOneField(Users, on_delete=models.DO_NOTHING, primary_key=True, db_column='employee_number')

    class Meta:
        managed = False
        db_table = 'Salesperson'


# ---------------- TRANSACTIONS ----------------

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_due_date = models.DateField(blank=True, null=True)
    transaction_status = models.CharField(max_length=50, blank=True, null=True)
    transaction_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sales = models.ForeignKey(Salesperson, on_delete=models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Transactions'


class TransactionLine(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    line_number = models.IntegerField()
    quantity = models.IntegerField()
    unit_price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'TransactionLine'
        unique_together = (('transaction', 'product'),)


# ---------------- INVENTORY ----------------

class BranchInventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'BranchInventory'
        unique_together = (('branch', 'product'),)


# ---------------- SUPPLY CHAIN ----------------

class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    shipment_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    shipment_status = models.CharField(max_length=50, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, blank=True, null=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.DO_NOTHING, blank=True, null=True, db_column= 'vehicle_id')

    class Meta:
        managed = False
        db_table = 'Shipment'


class PurchaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    employee_number = models.ForeignKey(Manager, on_delete=models.DO_NOTHING, db_column='employee_number')
    order_date = models.DateField(blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PurchaseOrder'


class ReceivesProductsFrom(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ReceivesProductsFrom'
        unique_together = (('supplier', 'branch'),)
