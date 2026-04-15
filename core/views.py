# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Customer, Product, Branch, HasInventoryOf, Supplier, Transaction, TransactionLine, CustomerPurchase, PurchaseOrder, ReceivesProductsFrom
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

# ===================== Add Customer =====================
@csrf_exempt
def add_customer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        customer = Customer.objects.create(
            CustomerID=data["CustomerID"],
            ContactInfo=data["ContactInfo"],
            CustomerName=data["CustomerName"]
        )
        return JsonResponse({"status": "success", "CustomerID": customer.CustomerID})
    return JsonResponse({"error": "POST required"}, status=400)

# ===================== Add Product =====================
@csrf_exempt
def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product = Product.objects.create(
            ProductID=data["ProductID"],
            ProductName=data["ProductName"],
            ProductDescription=data.get("ProductDescription", ""),
            UnitPrice=data["UnitPrice"]
        )
        return JsonResponse({"status": "success", "ProductID": product.ProductID})
    return JsonResponse({"error": "POST required"}, status=400)

# ===================== Update Customer =====================
@csrf_exempt
def update_customer(request, customer_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            customer = Customer.objects.get(CustomerID=customer_id)
            customer.ContactInfo = data.get("ContactInfo", customer.ContactInfo)
            customer.CustomerName = data.get("CustomerName", customer.CustomerName)
            customer.save()
            return JsonResponse({"status": "success"})
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)
    return JsonResponse({"error": "PUT required"}, status=400)

# ===================== Update Product =====================
@csrf_exempt
def update_product(request, product_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            product = Product.objects.get(ProductID=product_id)
            product.ProductName = data.get("ProductName", product.ProductName)
            product.ProductDescription = data.get("ProductDescription", product.ProductDescription)
            product.UnitPrice = data.get("UnitPrice", product.UnitPrice)
            product.save()
            return JsonResponse({"status": "success"})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
    return JsonResponse({"error": "PUT required"}, status=400)

# ===================== Delete Product =====================
@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        try:
            product = Product.objects.get(ProductID=product_id)
            product.delete()
            return JsonResponse({"status": "deleted"})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
    return JsonResponse({"error": "DELETE required"}, status=400)

# ===================== View Products =====================
def view_products(request):
    products = Product.objects.all()
    data = [{"ProductID": p.ProductID, "ProductName": p.ProductName, "ProductDescription": p.ProductDescription, "UnitPrice": p.UnitPrice} for p in products]
    return JsonResponse(data, safe=False)

# ===================== View Branch Inventory =====================
def view_branch_inventory(request):
    inventory = []
    for h in HasInventoryOf.objects.all():
        inventory.append({
            "BranchID": h.BranchID.BranchID,
            "Address": h.BranchID.Address,
            "ProductID": h.ProductID.ProductID,
            "ProductName": h.ProductID.ProductName,
            "NumProducts": h.NumProducts
        })
    return JsonResponse(inventory, safe=False)

# ===================== Monitor Stock Levels =====================
def monitor_stock_levels(request):
    stock = []
    for h in HasInventoryOf.objects.all():
        stock.append({
            "ProductID": h.ProductID.ProductID,
            "ProductName": h.ProductID.ProductName,
            "NumProducts": h.NumProducts
        })
    return JsonResponse(stock, safe=False)

# ===================== Update Inventory Records =====================
@csrf_exempt
def update_inventory(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            h = HasInventoryOf.objects.get(BranchID=data["old_branch_id"], ProductID=data["ProductID"])
            h.BranchID = Branch.objects.get(BranchID=data["new_branch_id"])
            h.save()
            return JsonResponse({"status": "success"})
        except HasInventoryOf.DoesNotExist:
            return JsonResponse({"error": "Inventory record not found"}, status=404)
    return JsonResponse({"error": "PUT required"}, status=400)

# ===================== Add Supplier =====================
@csrf_exempt
def add_supplier(request):
    if request.method == "POST":
        data = json.loads(request.body)
        supplier = Supplier.objects.create(
            SupplierID=data["SupplierID"],
            Address=data.get("Address", ""),
            ContactInfo=data.get("ContactInfo", "")
        )
        return JsonResponse({"status": "success", "SupplierID": supplier.SupplierID})
    return JsonResponse({"error": "POST required"}, status=400)

# ===================== Update Supplier =====================
@csrf_exempt
def update_supplier(request, supplier_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            supplier = Supplier.objects.get(SupplierID=supplier_id)
            supplier.Address = data.get("Address", supplier.Address)
            supplier.ContactInfo = data.get("ContactInfo", supplier.ContactInfo)
            supplier.save()
            return JsonResponse({"status": "success"})
        except Supplier.DoesNotExist:
            return JsonResponse({"error": "Supplier not found"}, status=404)
    return JsonResponse({"error": "PUT required"}, status=400)

# ===================== Delete Supplier =====================
@csrf_exempt
def delete_supplier(request, supplier_id):
    if request.method == "DELETE":
        try:
            supplier = Supplier.objects.get(SupplierID=supplier_id)
            supplier.delete()
            return JsonResponse({"status": "deleted"})
        except Supplier.DoesNotExist:
            return JsonResponse({"error": "Supplier not found"}, status=404)
    return JsonResponse({"error": "DELETE required"}, status=400)