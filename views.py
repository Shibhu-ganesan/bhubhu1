from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from django.contrib import messages
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import OrderForm, CustomerForm, CreateUserForm
from .decorator import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(req):
    order = req.user.customer.status_set.all()
    orders = Status.objects.all()
    total_orders = order.count()
    status_delivered = order.filter(status='delivered').count()
    status_pending = order.filter(status='pending').count()
    context = {'orders':order, 'total_orders':total_orders,'delivered':status_delivered, 'pending':status_pending}
    return render(req, 'dennisapp/user.html', context)

@unauthenticated_user
def loginn(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('dashboard')
        else:
            messages.info(req, 'Username or password is incorrect')
    context = {}
    return render(req, 'dennisapp/login.html', context)


def logoutt(req):
    logout(req)
    return redirect('login')

@unauthenticated_user
def register(req):
    if req.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if req.method == 'POST':
            form = CreateUserForm(req.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(req, 'User ' + username + ' is successfully created')
                return redirect('login')
        context = {'form': form}
        return render(req, 'dennisapp/register.html', context)

@login_required(login_url='login')
def customer(req, number):
    customers = Customer.objects.get(id=number)
    orders = customers.status_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(req.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customers': customers, 'orders':orders, 'totalorder': orders_count, 'myfilter':myFilter}
    return render(req,'dennisapp/customer.html', context)

@login_required(login_url='login')
def products(req):
    products = Product.objects.all()
    return render(req,'dennisapp/products.html',{'products': products})

@login_required(login_url='login')
@admin_only
def dashboard(req):
    customers = Customer.objects.all()
    orders = Status.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    status_delivered = orders.filter(status='delivered').count()
    status_pending = orders.filter(status='pending').count()
    context = {'customers': customers, 'orders': orders, 'total_customers': total_customers, 'total_orders': total_orders, 'pending':status_pending, 'delivered':status_delivered}
    return render(req, 'dennisapp/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def dennisform(req, customerid):
    OrderFormSet = inlineformset_factory(Customer, Status, fields=('product','status'))
    customers = Customer.objects.get(id=customerid)
    formset = OrderFormSet(queryset=Status.objects.none(), instance=customers)
    #form = OrderForm(initial = {'customer': customers})
    if req.method == 'POST':
        print("Printing post:", req.POST)
        formset = OrderFormSet(req.POST, instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'forms': formset }
    return render(req, 'dennisapp/forms.html', context)

@login_required(login_url='login')
@admin_only
def updateorderid(req,customerid):
    customer = Customer.objects.get(id=customerid)
    form =  OrderForm(initial={'customer':customer})
    if req.method == 'POST':
        # print("Printing post:", req.POST)
        form = OrderForm(req.POST,  instance = customer)
        if form.is_valid:
            form.save()
            return dashboard(req)
    context = {'forms': form}
    return render(req, 'dennisapp/forms.html', context)

@login_required(login_url='login')
@admin_only
def createcustomer(req):
    form =  CustomerForm()
    if req.method == 'POST':
        # print("Printing post:", req.POST)
        form = CustomerForm(req.POST)
        if form.is_valid:
            form.save()
            return dashboard(req)
    context = {'forms': form}
    return render(req, 'dennisapp/forms.html', context)

@login_required(login_url='login')
@admin_only
def updatedennisform(req, customerid):
    order = Status.objects.get(id=customerid)
    form = OrderForm(instance= order)
    if req.method == 'POST':
        form = OrderForm(req.POST, instance = order)
        if form.is_valid:
            form.save()
            return dashboard(req)
    context = {'forms':form}
    return render(req, 'dennisapp/forms.html', context)

@login_required(login_url='login')
@admin_only
def deleteitem(req, deleteid):
    order = Status.objects.get(id=deleteid)
    if req.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(req,'dennisapp/delecs.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def settings(req):
    customer = req.user.customer
    form = CustomerForm(instance=customer)
    if req.method=='POST':
        form = CustomerForm(req.POST,req.FILES, instance=customer)
        if form.is_valid:
            form.save()
            return redirect('settings')
    context = {'form':form}
    return render(req,'dennisapp/settings.html', context)





