from django import forms
from .models import Customer,Order

class CustomerForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=  Customer
        fields = ('username', 'email', 'password', 'phone', 'address', 'city')

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'phone_optional', 'address', 'address_optional', 'city')