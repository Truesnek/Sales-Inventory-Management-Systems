from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_branch_carrier_supplier_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPurchase',
            fields=[
                ('customer_purchase_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('purchase_order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('shipment_id', models.AutoField(primary_key=True, serialize=False)),
                ('shipment_date', models.DateTimeField()),
            ],
        ),
    ]
