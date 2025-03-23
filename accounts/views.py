from django.shortcuts import render, redirect
from .models import Products, Customer, Order
from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group

# Create your views here.


@unauthenticated_user
def registerPage(request):  
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')

    context={
        'form':form
    }
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@allowed_user(allow_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_order': total_order,
        'total_delivered': total_delivered,
        'total_pending': total_pending
    }
    return render(request, 'accounts/user.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else: 
            messages.info(request, f'Wrong Username or Password')
    context={

    }
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customer = customers.count()
    total_order = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'total_customer': total_customer,
        'total_order': total_order,
        'total_delivered': total_delivered,
        'total_pending': total_pending
    }


    return render(request, 'accounts/dashboard.html', context)  # account in template

@login_required(login_url='login')
@allowed_user(allow_roles=['admin'])
def product(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_user(allow_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)  # Get the customer by id (pk)
    orders = customer.order_set.all()  # Get all orders related to this customer
    orders_count = orders.count()  # Count the number of orders

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'myFilter': myFilter,
        'customer': customer,  # Pass the customer object to the template
        'orders': orders,
        'orders_count': orders_count
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_user(allow_roles=['admin'])
def create_order(request, pk):
    # Get the customer by primary key (pk)
    customer = Customer.objects.get(id=pk)

    # Create an inline formset factory
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('products', 'status'), extra=3)

    # Handle GET request: Show empty formset with initial 1 empty form
    if request.method == 'GET':
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    
    # Handle POST request: Save formset data
    elif request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()  # Save the valid formset data
            return redirect('/')  # Redirect to home or another page

    context = {
        'form': formset,
        'customer': customer,
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allow_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allow_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context={
        'item': order,
    }
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_user(allow_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Information has been changed successfully!')
            return redirect('user_page')  # Redirects after successful update
    context={
        'form': form,
    }
    return render(request, 'accounts/account_settings.html', context)