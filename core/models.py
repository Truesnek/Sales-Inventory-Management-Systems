from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    unit_price = models.FloatField()

    def __str__(self):
        return self.product_name
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_status = models.CharField(max_length=50)
    total_amount = models.FloatField()
    transaction_date = models.DateTimeField()
    transaction_due_date = models.DateTimeField()
    transaction_discount = models.FloatField()

    def __str__(self):
        return f"Transaction {self.transaction_id}"

class TransactionLine(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    line_number = models.IntegerField()
    quantity = models.IntegerField()
    unit_price_at_sale = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('transaction', 'line_number')

    def __str__(self):
        return f"Transaction {self.transaction.transaction_id} - Line {self.line_number}"

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=150)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return f"Supplier {self.supplier_id}"


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f"Branch {self.branch_id}"
    

class Carrier(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    carrier_type = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)

    def __str__(self):
        return f"Carrier {self.vehicle_id}"

class Users(models.Model):
    employee_num = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.employee_num}"
    
class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    shipment_date = models.DateTimeField()
    estimated_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField()
    shipment_status = models.CharField(max_length=50)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shipment {self.shipment_id}"
class PurchaseOrder(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)
    order_id = models.IntegerField()

    def __str__(self):
        return f"PurchaseOrder {self.order_id}"
class CustomerPurchase(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)
    sales_id = models.IntegerField()

    def __str__(self):
        return f"CustomerPurchase {self.sales_id}"
class Manager(models.Model):
    employee_num = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="employee_num",
    )

    def __str__(self):
        return f"Manager {self.employee_num_id}"
class Salesperson(models.Model):
    employee_num = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="employee_num",
    )

    def __str__(self):
        return f"Salesperson {self.employee_num_id}"
class Shipper(models.Model):
    employee_num = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="employee_num",
    )

    def __str__(self):
        return f"Shipper {self.employee_num_id}"

class HasInventoryOf(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num_products = models.IntegerField()

    class Meta:
        unique_together = ('branch', 'product')

    def __str__(self):
        return f"{self.branch.branch_id} - {self.product.product_id}"

class IsPaidBy(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('branch', 'customer')

    def __str__(self):
        return f"{self.branch_id} - {self.customer_id}"

class TransportedIn(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, to_field='vehicle_id')

    class Meta:
        unique_together = ('shipment', 'carrier')

    def __str__(self):
        return f"{self.shipment.shipment_id} - {self.carrier.vehicle_id}"

class Creates(models.Model):
    employee_num = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column="employee_num")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    class Meta:
        unique_together = ('employee_num', 'transaction', 'order_id')

    def __str__(self):
        return f"{self.employee_num_id} - {self.transaction_id} - {self.order_id}"

class Tracks(models.Model):
    employee_num = models.ForeignKey(Shipper, on_delete=models.CASCADE, db_column="employee_num")
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employee_num', 'shipment')

    def __str__(self):
        return f"{self.employee_num_id} - {self.shipment_id}"

class Sells(models.Model):
    employee_num = models.ForeignKey(Salesperson, on_delete=models.CASCADE, db_column="employee_num")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    sales_id = models.IntegerField()

    class Meta:
        unique_together = ('employee_num', 'transaction', 'sales_id')

    def __str__(self):
        return f"{self.employee_num_id} - {self.transaction_id} - {self.sales_id}"


class GivesProductsTo(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    sales_id = models.IntegerField()

    class Meta:
        unique_together = ('branch', 'transaction', 'sales_id')

    def __str__(self):
        return f"{self.branch_id} - {self.transaction_id} - {self.sales_id}"


class MakesPaymentTo(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('branch', 'supplier')

    def __str__(self):
        return f"{self.branch_id} - {self.supplier_id}"


class ReceivesProductsFrom(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('branch', 'transaction', 'order_id', 'supplier')

    def __str__(self):
        return f"{self.branch_id} - {self.transaction_id} - {self.order_id} - {self.supplier_id}"