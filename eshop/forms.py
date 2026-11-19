from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter product name'}),
            'price':forms.NumberInput(attrs={'class':'form-control','placeholder':'enter product price'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'enter product description'}),
            'image':forms.FileInput(attrs={'class':'form-control'})

        }
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name']