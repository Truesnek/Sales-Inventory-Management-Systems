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
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f"Transaction {self.transaction_id}"


class TransactionLine(models.Model):
    transaction_line_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)