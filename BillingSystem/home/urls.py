from django.urls import path
from home import views

urlpatterns = [
    path("", views.loginPage, name='loginpage'),
    path("register", views.register, name='register'),
    path("login", views.loginuser, name='login'),
    path('logout', views.logout_user, name='logout'),
    path("home",views.index,name='home'),
    path("customer",views.customer,name='customer'),
    path("product",views.product,name='product'),
   
    path('404/', views.error_404_view, name='error_404'),
    path("add-customer",views.add_customer,name='add-customer'),
    path("delete-customer/<int:customer_id>",views.delete_customer,name='delete-customer'),
    path("update-customer/<int:customer_id>", views.update_customer, name='update-customer'),
    path("view-customer-details/<int:customer_id>", views.view_customer_details, name="view-customer-details"),
     
    path("add-product",views.add_product,name='add-product'),
    path("delete-product/<int:product_id>",views.delete_product,name='delete-product'),
    path("update-product/<int:product_id>",views.update_product,name='update-product'),
    
    path('bill/', views.bill_form, name='bill_form'),
    path('generate-bill/', views.generate_bill, name='generate_bill'),
    path('get-customer-name/', views.get_customer_name, name='get_customer_name'),
    path('add-to-bill/', views.add_to_bill, name='add_to_bill'),
    path('generate-invoice/', views.generate_invoice, name='generate_invoice'),
   
]