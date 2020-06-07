from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created for ' + username + '!')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'accounts/login.html', context)

# there is a better way to do this other than doing it for every restricted view
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only  # this is used instead of allowed_users so the home page to redirect non-admins to their profile; band aid
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def products(request):
    products_list = Product.objects.all()
    # 'products' as a dictionary key will have to match the template tag
    return render(request, "accounts/products.html", {'products': products_list})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)  # the name pk has to match the name pk in urls.py
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, "accounts/customer.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print("Printing POST: ", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()  # ModelForm will handle this
            return redirect('/')

    context = {'formset': formset, 'customer': customer}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # overwrite the instance
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, "accounts/delete.html", context)