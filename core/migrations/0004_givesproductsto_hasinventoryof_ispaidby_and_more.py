import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customerpurchase_purchaseorder_shipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='GivesProductsTo',
            fields=[
                ('gives_products_to_id', models.AutoField(primary_key=True, serialize=False)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shipment')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='HasInventoryOf',
            fields=[
                ('has_inventory_of_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='IsPaidBy',
            fields=[
                ('is_paid_by_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='MakesPaymentTo',
            fields=[
                ('makes_payment_to_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.purchaseorder')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.users')),
            ],
        ),
        migrations.CreateModel(
            name='Creates',
            fields=[
                ('creates_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.purchaseorder')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.manager')),
            ],
        ),
        migrations.CreateModel(
            name='ReceivesProductsFrom',
            fields=[
                ('receives_products_from_id', models.AutoField(primary_key=True, serialize=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.branch')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shipment')),
            ],
        ),
        migrations.CreateModel(
            name='Salesperson',
            fields=[
                ('salesperson_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.users')),
            ],
        ),
        migrations.CreateModel(
            name='Sells',
            fields=[
                ('sells_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customerpurchase')),
                ('salesperson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.salesperson')),
            ],
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('shipper_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.users')),
            ],
        ),
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('tracks_id', models.AutoField(primary_key=True, serialize=False)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shipment')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shipper')),
            ],
        ),
        migrations.CreateModel(
            name='TransportedIn',
            fields=[
                ('transported_in_id', models.AutoField(primary_key=True, serialize=False)),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carrier')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shipment')),
            ],
        ),
    ]
