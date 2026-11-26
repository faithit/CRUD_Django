from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductForm,RegisterForm
from .models import Product
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Avg, Count, Sum
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request, 'home.html',{'products':products})
#r-read-fetch records from db
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    analytics = Product.objects.aggregate(
        total_products=Count('id'),
        catalog_value=Sum('price'),
        average_price=Avg('price'),
    )
    analytics['added_last_7_days'] = Product.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    return render(request, 'admin_dashboard.html',{
        'products': products,
        'analytics': analytics,
    })
#crud-c-create-add a record
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
def add_product(request):
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form=ProductForm()
    return render(request, 'add_product.html',{'form':form})
    #d-delete. delete a record from db
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
@require_POST
def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return redirect('products')
#u-update an existing record
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
def update_product(request,id):
    product=get_object_or_404(Product,id=id)
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form=ProductForm(instance=product)
    return render(request,'add_product.html',{'form':form})
#register users
def register_user(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()#saves to db the user
            return redirect('home')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})
def login_user(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
             user=form.get_user()
             login(request,user)
             if user.is_staff:
                 return redirect('products')
             else:
                 return redirect('user')           
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

@login_required(login_url='login')
#navigates user to  dashboard
def user_dashboard(request):
    return render(request,'users/user_dashboard.html')
#logouts user
def logout_user(request):
    logout(request)
    return redirect('login')
