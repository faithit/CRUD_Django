from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductForm,RegisterForm
from .models import Product


# Create your views here.
def home(request):
    return render(request, 'home.html')
#r-read-fetch records from db
def products(request):
    products=Product.objects.all()
    return render(request, 'admin_dashboard.html',{'products':products})
#crud-c-create-add a record
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
def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return redirect('products')
#u-update an existing record
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
    form=RegisterForm()
    return render(request,'register.html',{'form':form})
