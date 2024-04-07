
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect,render

from home.models import Customer, emp_detail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, authenticate



@login_required
def index(request):
     products = Product.objects.all()  # Retrieve all products from the database
     context = {'products': products} 
     return render(request,'mainpage.html',context)


def loginPage(request):
    return render(request,'login.html')



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
       
        # Check if the email is already used as a username
        if emp_detail.objects.filter(username=email).exists():
            messages.success(request, 'Email already in use. Please choose a different email.')
            return render(request, 'index.html')
            # print("Before clearing messages:", request.COOKIES.get('messages'))
            # clear_messages(request)
            # print("After clearing messages:", request.COOKIES.get('messages'))
        
        else:
            user = emp_detail.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            if user:
                messages.success(request, 'Employee Details Added Successfully')
                return redirect('register')
    return render(request, 'register.html')

def loginuser(request):
    if request.method=='POST':
        username=request.POST['username']
        password =request.POST['password']
        # print(username,password)
        user = authenticate(request,username=username,password = password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home')  
            else:
                return redirect('home')
        else:
             messages.success(request, 'Invalid User')
             return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('loginpage')


@login_required
def customer(request):
    customers = Customer.objects.all()  # Retrieve all customers from the database
    context = {'customers': customers}  # Pass customers to the template context
    return render(request, 'Customer.html', context)


@login_required
def product(request):
    products = Product.objects.all()  # Retrieve all products from the database
    context = {'products': products}  # Pass products to the template context
    return render(request, 'product.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phn_no = request.POST.get('phn_no')
        city = request.POST.get('city')
        
        # Create new customer object and save it
        Customer.objects.create(name=name, age=age, email=email, phn_no=phn_no, city=city)
        return redirect('customer')  # Redirect to customer page after adding
        
    return render(request, 'add_customer.html')  # Render add customer form template


@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer')
    return render(request, 'delete_customer.html', {'customer': customer})


@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.age = request.POST.get('age')
        customer.email = request.POST.get('email')
        customer.phn_no = request.POST.get('phn_no')
        customer.city = request.POST.get('city')
        customer.save()
        return redirect('customer')
    return render(request, 'update_customer.html', {'customer': customer})


@login_required
def view_customer_details(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'customer_details.html', {'customer': customer})    



from .models import Bill, Product

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        product = Product.objects.create(name=name, price=price, brand=brand)
        return redirect('product')  # Redirect to the product list page after adding product
    return render(request, 'add_product.html')


@login_required
def update_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.brand = request.POST.get('brand')
        product.save()
        return redirect('product')  # Redirect to the product list page after updating product
    return render(request, 'update_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('product')  # Redirect to the product list page after deleting product


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


from django.http import HttpResponse, JsonResponse



@login_required
def bill_form(request):
    employee_name = request.user.get_full_name()
    return render(request, 'bill_form.html', {'employee_name': employee_name})



# @login_required
# def generate_bill(request):
#     if request.method == 'GET':
#         phone_number = request.GET.get('phone_number')
#         print("Received phone number:", phone_number)  # Debugging statement
#         try:
#             customer = Customer.objects.get(phn_no=phone_number)
#             customer_name = customer.name
#             # Here you can proceed with generating the bill and displaying the invoice
#             return HttpResponse(f"Bill generated for customer: {customer_name}")
#         except Customer.DoesNotExist:
#             return HttpResponse("Customer with the provided phone number does not exist. Please register the customer.")
#     else:
#         return HttpResponse("Method not allowed")

from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Product

from django.shortcuts import render, redirect
from .models import Customer, Bill, Product

def generate_bill(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phn_no')
        try:
            customer = Customer.objects.get(phn_no=phone_number)
            # Retrieve the logged-in employee
            employee = request.user
            # Create a new bill object
            bill = Bill.objects.create(customer=customer)
            # Retrieve the selected products and their quantities
            for product in Product.objects.all():
                quantity_key = f'quantity{product.product_id}'
                quantity = int(request.POST.get(quantity_key, 0))
                if quantity > 0:
                    bill.products.add(product, through_defaults={'quantity': quantity})
            # Calculate total amount
            total_amount = sum(product.price * item.quantity for item in bill.products.through.objects.filter(bill=bill))
            bill.bill_amount = total_amount
            bill.save()
            # Render the invoice template with bill details
            return render(request, 'invoice.html', {'bill': bill})
        except Customer.DoesNotExist:
            error_message = "Customer with the provided phone number does not exist. Please register the customer."
            return render(request, 'invoice.html', {'error_message': error_message})
    else:
        return render(request, 'invoice.html')
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Bill
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_customer_name(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phn_no')
        try:
            customer = get_object_or_404(Customer, phn_no=phone_number)
            return JsonResponse({'name': Customer.name})
        except:
            return JsonResponse({'error': 'Customer not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def add_to_bill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data['product_name']
        product_price = float(data['product_price'])
        quantity = int(data['quantity'])
        customer_phone = data['customer_phone']
        
        

        try:
            customer = Customer.objects.get(phn_no=customer_phone)
            # Calculate the amount
            amount = product_price * quantity
            current_time = timezone.now()
            # Create a new Bill object and save it to the database
            bill = Bill.objects.create(bill_amount=amount, customer=customer,timestamp = current_time)
            
            # Add the product to the bill
            product = Product.objects.get(name=product_name)
            
            bill.products.add(product, through_defaults={'quantity': quantity})

            return JsonResponse({'message': 'Item added to bill successfully'})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

@csrf_exempt
def generate_invoice(request):
    if request.method == 'POST':
        # Retrieve all bill items from the database
        bill_items = Bill.objects.all()
        total_amount = sum(item.amount for item in bill_items)
        # Assuming employee name and customer name are provided in the request or fetched from somewhere else
        employee_name = "John Doe"  # Replace with actual logic to get employee name
        customer_name = "Some Customer"  # Replace with actual logic to get customer name
        # Pass necessary data to the template for rendering
        return render(request, 'invoice.html', {
            'employee_name': employee_name,
            'customer_name': customer_name,
            'bill_items': bill_items,
            'total_amount': total_amount,
        })

