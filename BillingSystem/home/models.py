from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class emp_detail(User):
    emp_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=200)
    def __str__(self):
        return self.email
    
# In models.py



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phn_no = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product) 
    timestamp = models.DateTimeField(default=timezone.now)# Many-to-many relationship with Product

    def __str__(self):
        return f'Bill - {self.bill_id}'