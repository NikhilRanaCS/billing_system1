from django.contrib import admin
from django.contrib import admin
from .models import Bill, Customer, Product, emp_detail   # Import the model from your home app

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Bill)# Register the model in the admin site
