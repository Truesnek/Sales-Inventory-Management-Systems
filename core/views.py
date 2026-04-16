# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

import json
from .models import Customer, Products, Branch, BranchInventory, Supplier, Transactions, TransactionLine, PurchaseOrder, ReceivesProductsFrom,Salesperson,Shipment
from sales_inventory_management import urls

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
                return redirect("sales-home")
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

    total_products = Products.objects.count()
    total_suppliers = Supplier.objects.count()
    total_transactions = Transactions.objects.count()
    total_customers = Customer.objects.count()
    total_shipments = Shipment.objects.count()

    return render(request, "GenerateReport.html", {
        "username": username,
        "total_products": total_products,
        "total_suppliers": total_suppliers,
        "total_transactions": total_transactions,
        "total_customers": total_customers,
        "total_shipments": total_shipments,
    })


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
            "num_products": p.num_products,
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
    inventory = (
        BranchInventory.objects.select_related("branch", "product")
        .all()
        .order_by("branch__branch_id", "product__product_id")
    )

    data = [
        {
            "branch_id": item.branch.branch_id,
            "address": item.branch.address,
            "product_id": item.product.product_id,
            "product_name": item.product.product_name,
            "quantity": item.quantity,
        }
        for item in inventory
    ]

    return JsonResponse(data, safe=False)


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