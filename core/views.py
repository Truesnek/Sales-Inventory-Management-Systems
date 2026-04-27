# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db import connection

import json
from .models import Customer, Products, Branch, BranchInventory, Supplier, Transactions, TransactionLine, PurchaseOrder, ReceivesProductsFrom,Salesperson,Shipment
from sales_inventory_management import urls

# View for Branch Inventory page
def branch_inventory_view(request):
    return render(request, 'branch_inventory.html')

# View for Manage Customers page
def manage_customers_view(request):
    return render(request, 'manage_customers.html')

# View for Record Customer Purchase page
def record_purchase_view(request):
    return render(request, 'record_purchase.html')

# View for Transaction History page
def transaction_history_view(request):
    return render(request, 'transaction_history.html')


# Predefined credentials
VALID_USERS = {
    "Manager": "Password",
    "SalesPerson": "Password"
}

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username in VALID_USERS and password == VALID_USERS[username]:
            request.session['username'] = username
            request.session['role'] = "Manager" if username == "Manager" else "SalesPerson"

            # Redirect based on role
            if username == "Manager":
                return redirect("manage-products")
            else:
                return redirect("manage_customers")
        else:
            return render(request, "login.html", {"error": "Invalid username or password", 
                                                  "username": username, 
                                                  "password": ""})
    
    # Prefill for simulation
    return render(request, "login.html", {"username": "Manager", "password": "Password"})

def manage_products(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, "ManageProduct.html", {"username": username})

def manage_inventory(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    inventory = BranchInventory.objects.select_related("branch", "product").all().order_by(
        "branch__branch_id", "product__product_id"
    )

    return render(request, "ManageBranchInventory.html", {
        "username": username,
        "inventory": inventory,
    })


def manage_suppliers(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    suppliers = Supplier.objects.all().order_by("supplier_id")

    return render(request, "ManageSuppliers.html", {
        "username": username,
        "suppliers": suppliers,
    })


def create_purchase_order_page(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    purchase_orders = PurchaseOrder.objects.select_related("employee_number").all().order_by("order_id")

    return render(request, "CreatePurchaseOrder.html", {
        "username": username,
        "purchase_orders": purchase_orders,
    })


def generate_report_page(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    products = Products.objects.all().order_by("product_id")
    suppliers = Supplier.objects.all().order_by("supplier_id")
    shipments = Shipment.objects.select_related("supplier", "branch", "carrier").all().order_by("-shipment_id")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                bi.branch_id,
                b.address,
                bi.product_id,
                p.product_name,
                bi.quantity
            FROM BranchInventory bi
            JOIN Branch b ON bi.branch_id = b.branch_id
            JOIN Products p ON bi.product_id = p.product_id
            ORDER BY bi.branch_id, bi.product_id
        """)
        inventory = [
            {
                "branch_id": row[0],
                "address": row[1],
                "product_id": row[2],
                "product_name": row[3],
                "quantity": row[4],
            }
            for row in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT
                t.transaction_id,
                t.transaction_status,
                t.total_amount,
                t.transaction_date,
                c.customer_name,
                t.sales_id
            FROM Transactions t
            LEFT JOIN Customer c ON t.customer_id = c.customer_id
            ORDER BY t.transaction_id DESC
        """)
        transactions = [
            {
                "transaction_id": row[0],
                "transaction_status": row[1],
                "total_amount": row[2],
                "transaction_date": row[3],
                "customer_name": row[4],
                "sales_id": row[5],
            }
            for row in cursor.fetchall()
        ]

    context = {
        "username": username,
        "total_products": products.count(),
        "total_suppliers": suppliers.count(),
        "total_transactions": len(transactions),
        "total_customers": Customer.objects.count(),
        "total_shipments": shipments.count(),
        "total_inventory_records": len(inventory),
        "products": products,
        "suppliers": suppliers,
        "transactions": transactions,
        "shipments": shipments,
        "inventory": inventory,
    }

    return render(request, "GenerateReport.html", context)


def manage_customers(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    customers = Customer.objects.all()
    return render(request, "ManageCustomers.html", {"customers": customers})


def manage_transactions(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    transactions = Transactions.objects.select_related("customer", "sales").all()
    return render(request, "ManageTransactions.html", {"transactions": transactions})


def manage_shipments(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    shipments = Shipment.objects.select_related("supplier", "branch", "carrier").all()
    return render(request, "ManageShipments.html", {"shipments": shipments})

# -------------------------
# Product API endpoints
# -------------------------

@csrf_exempt
@require_http_methods(["GET"])
def view_products(request):
    products = Products.objects.all().order_by("product_id")
    data = [
        {
            "product_id": p.product_id,
            "product_name": p.product_name,
            "product_description": p.product_description,
            "unit_price": str(p.unit_price),
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def add_product(request):
    data = json.loads(request.body)

    product = Products.objects.create(
        product_name=data["product_name"],
        product_description=data.get("product_description"),
        unit_price=data["unit_price"],
        num_products=data.get("num_products"),
    )

    return JsonResponse(
        {"status": "success", "product_id": product.product_id},
        status=201,
    )


@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, product_id):
    data = json.loads(request.body)
    product = get_object_or_404(Products, pk=product_id)

    product.product_name = data.get("product_name", product.product_name)
    product.product_description = data.get(
        "product_description",
        product.product_description,
    )
    product.unit_price = data.get("unit_price", product.unit_price)
    product.num_products = data.get("num_products", product.num_products)
    product.save()

    return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    product.delete()
    return JsonResponse({"status": "deleted"})


# -------------------------
# Customer API endpoints
# -------------------------

@csrf_exempt
@require_http_methods(["POST"])
def add_customer(request):
    data = json.loads(request.body)

    customer = Customer.objects.create(
        customer_name=data["customer_name"],
        contact_info=data.get("contact_info"),
    )

    return JsonResponse(
        {"status": "success", "customer_id": customer.customer_id},
        status=201,
    )


@csrf_exempt
@require_http_methods(["PUT"])
def update_customer(request, customer_id):
    data = json.loads(request.body)
    customer = get_object_or_404(Customer, pk=customer_id)

    customer.customer_name = data.get("customer_name", customer.customer_name)
    customer.contact_info = data.get("contact_info", customer.contact_info)
    customer.save()

    return JsonResponse({"status": "success"})


# -------------------------
# Inventory API endpoints
# -------------------------

@csrf_exempt
@require_http_methods(["GET"])
def view_branch_inventory(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                bi.branch_id,
                b.address,
                bi.product_id,
                p.product_name,
                bi.quantity
            FROM BranchInventory bi
            JOIN Branch b ON bi.branch_id = b.branch_id
            JOIN Products p ON bi.product_id = p.product_id
            ORDER BY bi.branch_id, bi.product_id
        """)

        inventory = [
            {
                "branch_id": row[0],
                "address": row[1],
                "product_id": row[2],
                "product_name": row[3],
                "quantity": row[4],
            }
            for row in cursor.fetchall()
        ]

    return JsonResponse(inventory, safe=False)



@csrf_exempt
@require_http_methods(["PUT"])
def update_inventory(request):
    data = json.loads(request.body)

    item = get_object_or_404(
        BranchInventory,
        branch_id=data["branch_id"],
        product_id=data["product_id"],
    )

    item.quantity = data["quantity"]
    item.save()

    return JsonResponse({"status": "success"})


# -------------------------
# Supplier API endpoints
# -------------------------

@csrf_exempt
@require_http_methods(["POST"])
def add_supplier(request):
    data = json.loads(request.body)

    supplier = Supplier.objects.create(
        address=data.get("address"),
        contact_info=data.get("contact_info"),
    )

    return JsonResponse(
        {"status": "success", "supplier_id": supplier.supplier_id},
        status=201,
    )


@csrf_exempt
@require_http_methods(["PUT"])
def update_supplier(request, supplier_id):
    data = json.loads(request.body)
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    supplier.address = data.get("address", supplier.address)
    supplier.contact_info = data.get("contact_info", supplier.contact_info)
    supplier.save()

    return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    supplier.delete()
    return JsonResponse({"status": "deleted"})


# -------------------------
# Transaction API endpoints
# -------------------------

@csrf_exempt
@require_http_methods(["GET"])
def view_transactions(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                transaction_id,
                transaction_date,
                transaction_due_date,
                transaction_status,
                transaction_discount,
                total_amount
            FROM Transactions
            ORDER BY transaction_id DESC
        """)

        transactions = [
            {
                "transaction_id": row[0],
                "transaction_date": row[1],
                "transaction_due_date": row[2],
                "transaction_status": row[3],
                "transaction_discount": row[4],
                "total_amount": row[5],
            }
            for row in cursor.fetchall()
        ]

    return JsonResponse(transactions, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_transaction(request):
    data = json.loads(request.body)

    with transaction.atomic():
        customer = get_object_or_404(Customer, pk=data["customer_id"])
        salesperson = get_object_or_404(Salesperson, pk=data["salesperson_id"])

        txn = Transactions.objects.create(
            customer=customer,
            sales=salesperson,
            transaction_status=data.get("transaction_status"),
            total_amount=data.get("total_amount"),
            transaction_date=data.get("transaction_date"),
            transaction_due_date=data.get("transaction_due_date"),
            transaction_discount=data.get("transaction_discount"),
        )

        for line in data.get("lines", []):
            product = get_object_or_404(Products, pk=line["product_id"])

            TransactionLine.objects.create(
                transaction=txn,
                product=product,
                line_number=line["line_number"],
                quantity=line["quantity"],
                unit_price_at_sale=line["unit_price_at_sale"],
            )

    return JsonResponse(
        {"status": "success", "transaction_id": txn.transaction_id},
        status=201,
    )

@csrf_exempt
@require_http_methods(["POST"])
def create_purchase_order(request):
    """
    API endpoint to create a transaction, transaction lines, and a purchase order.
    Expects JSON data like:
    {
        "total_amount": 1000.50,
        "transaction_date": "2026-04-18",
        "transaction_due_date": "2026-04-25",
        "transaction_discount": 50.0,
        "lines": [
            {"product_id": 1, "line_number": 1, "quantity": 2, "unit_price_at_sale": 200.0},
            {"product_id": 2, "line_number": 2, "quantity": 1, "unit_price_at_sale": 600.5}
        ],
        "employee_number": 1,
        "order_status": "New"
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        with transaction.atomic():
            #  Create the transaction
            txn = Transactions.objects.create(
                transaction_status="Pending",
                total_amount=data.get("total_amount"),
                transaction_date=data.get("transaction_date"),
                transaction_due_date=data.get("transaction_due_date"),
                transaction_discount=data.get("transaction_discount"),
            )

            #  Create transaction lines
            for line in data.get("lines", []):
                product = get_object_or_404(Products, pk=line["product_id"])
                TransactionLine.objects.create(
                    transaction=txn,
                    product=product,
                    line_number=line["line_number"],
                    quantity=line["quantity"],
                    unit_price_at_sale=line["unit_price_at_sale"],
                )

            #  Create purchase order linked to transaction
            manager = get_object_or_404(Manager, pk=data["employee_number"])
            po = PurchaseOrder.objects.create(
                transaction_id=txn,
                employee_number=manager,
                order_date=data.get("transaction_date"),
                order_status=data.get("order_status"),
            )

        return JsonResponse({
            "status": "success",
            "transaction_id": txn.transaction_id,
            "purchase_order_id": po.order_id
        }, status=201)

    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

def list_purchase_orders(request):
    orders = PurchaseOrder.objects.all().values('order_id', 'order_status')
    return JsonResponse(list(orders), safe=False)

def get_purchase_order(request, order_id):
    po = PurchaseOrder.objects.select_related('transaction_id').get(pk=order_id)
    txn = po.transaction_id
    lines = []
    if txn:
        lines = list(txn.transactionline_set.values('product_id', 'line_number', 'quantity', 'unit_price_at_sale'))
    po_data = {
        'order_id': po.order_id,
        'employee_number': po.employee_number_id,
        'order_date': str(po.order_date),
        'order_status': po.order_status,
        'transaction': {
            'transaction_id': txn.transaction_id,
            'transaction_date': str(txn.transaction_date),
            'transaction_due_date': str(txn.transaction_due_date),
            'transaction_status': txn.transaction_status,
            'transaction_discount': float(txn.transaction_discount) if txn.transaction_discount else 0,
            'total_amount': float(txn.total_amount) if txn.total_amount else 0,
            'lines': lines
        } if txn else None
    }
    return JsonResponse(po_data)

def update_purchase(request):
    po = PurchaseOrder.objects.select_related('transaction_id').get(pk=order_id)
    txn = po.transaction_id
    po.transaction_status = "Completed"
    po.save()
    lines = []
    
    if not txn:
        return JsonResponse({"success": True, "message": "No transaction lines to update"})

    lines = txn.transactionline_set.values_list('product_id', 'line_number', 'quantity', 'unit_price_at_sale')

    for line in lines:
        
        try:
            product = Product.objects.get(product_id=line[0])
            product.num_products += line[2]
            product.save()
        except Product.DoesNotExist:
            print("Product not found, cannot update")
    return JsonResponse({"success": True, "message": "Purchase order updated"})

@csrf_exempt
@require_http_methods(["GET"])
def generate_invoice(request, transaction_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                transaction_id,
                transaction_date,
                transaction_due_date,
                transaction_status,
                transaction_discount,
                total_amount
            FROM Transactions
            WHERE transaction_id = %s
        """, [transaction_id])

        transaction_row = cursor.fetchone()

        if not transaction_row:
            return JsonResponse({"error": "Transaction not found"}, status=404)
        cursor.execute("""
            SELECT
                tl.line_number,
                tl.product_id,
                p.product_name,
                tl.quantity,
                tl.unit_price_at_sale
            FROM TransactionLine tl
            JOIN Products p ON tl.product_id = p.product_id
            WHERE tl.transaction_id = %s
            ORDER BY tl.line_number
        """, [transaction_id])

        lines = [
            {
                "line_number": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "quantity": row[3],
                "unit_price_at_sale": float(row[4]),
                "line_total": float(row[3] * row[4]),
            }
            for row in cursor.fetchall()
        ]

    invoice = {
        "transaction_id": transaction_row[0],
        "transaction_date": str(transaction_row[1]),
        "transaction_due_date": str(transaction_row[2]),
        "transaction_status": transaction_row[3],
        "transaction_discount": float(transaction_row[4]) if transaction_row[4] else 0,
        "total_amount": float(transaction_row[5]) if transaction_row[5] else 0,
        "lines": lines,
    }
    return JsonResponse(invoice)
