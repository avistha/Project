from django.conf import Settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.db.models import Q
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm,OrderForm
from django.contrib.auth.models import User
from cart.cart import Cart
from django.http import HttpResponse

# Create your views here.

def index(request):
    data={
        'bannerData': Banner.objects.filter(is_active=True),
        'productsData': Product.objects.order_by('-id'),
    }
    return render(request, 'frontend/pages/index/index.html',data)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(subject, message, email, ['avinabshrestha1@gmail.com'])
        return redirect('contact')
    
    return render(request, 'frontend/pages/contact/contact.html')

def product_list(request):
    productData = Product.objects.order_by('-id')
    paginator = Paginator(productData, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data={
        'productsData': page_obj,
    }
    return render(request,'frontend/pages/product/product.html',data)

def product_details(request, slug):
    productData= Product.objects.get(slug=slug)
    categoryId = productData.category_id
    relatedData= Product.objects.filter(category_id=categoryId)
    data = {
        'productData': productData,
        'relatedData': relatedData,
    }
    return render(request, 'frontend/pages/product/details.html', data)

def product_category(request,slug):
    categoryData = Category.objects.get(slug=slug)
    productsData = Product.objects.filter(category_id=categoryData.id)
    data = {
        'productsData': productsData,
    }
    return render(request, 'frontend/pages/product/category.html',data)

def product_search(request):
    if request.method == "POST":
        criteria = request.POST['criteria']
        productsData = Product.objects.filter(Q(name__icontains=criteria) | Q(description__icontains=criteria))
        paginator = Paginator(productsData, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data={
            'productsData': page_obj,
        }
        return render(request, 'frontend/pages/product/product.html',data)

    else:
        return redirect('product')
    
def customer_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        user = User.objects.create_user(email=email, username=username, password=password)
        Customer.objects.create(user=user, phone=phone, address=address, city=city)
        messages.success(request, 'Registration successful.')
        return redirect('login')
    else:
        data = {
            'form' : CustomerForm(),
        }
        return render(request, 'frontend/pages/register/register.html', data)

def customer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials.')
            back = request.META.get('HTTP_REFERER')
            return redirect(back)
    else:
        data={
            'form': AuthenticationForm(),
        }
        return render(request, 'frontend/pages/login/login.html',data) 
    
def customer_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login')
def user_dashboard(request):
    login_id = request.user.id
    c_data=Customer.objects.get(user=login_id)
    order_data=Order.objects.filter(customer=c_data.id)
    data={
        'order_data':order_data,
    }
    return render(request, 'frontend/pages/user/dashboard.html',data)


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    total_price = 0 
    for key, value in request.session['cart'].items() : 
        total_price += float(value['price']) * int(value['quantity'])

    data = {
        'total_price' : total_price,
    }

    return render(request, 'frontend/pages/cart/cart_detail.html',data)

@login_required(login_url="/login")
def checkout(request):
    if request.method=="POST":
        total_price=0
        login_id = request.user.id
        customer = Customer.objects.get(user=login_id)
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_optional = request.POST['phone_optional']
        phone = request.POST['phone']
        address = request.POST['address']
        address_optional = request.POST['address_optional']
        city = request.POST['city']

        order = Order(customer=customer, total=total_price, full_name=full_name, email=email, address=address,
                       address_optional=address_optional, phone=phone, phone_optional=phone_optional, city=city)
        order.save()
        order_id = order.id

        for key, value in request.session['cart'].items() : 
            pid = value['product_id']
            product = Product.objects.get(id=pid)
            quantity = value['quantity']
            OrderItem.objects.create(order_id=order_id, product=product, quantity=quantity)

            total_price += float(value['price']) * int(value['quantity'])

        cart = Cart(request)
        cart.clear()
        messages.success(request, 'Order placed successfully')
        return redirect("index")

    else:
        total_price=0
        for key, value in request.session['cart'].items() : 
            total_price += float(value['price']) * int(value['quantity'])
        

    data = {
        'total_price' : total_price,
        'orderForm': OrderForm(),
    }

    return render(request, 'frontend/pages/cart/checkout.html',data)