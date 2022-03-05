from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import json 
import datetime

from .models import Items, Customer, Order, OrderItem, ShippingAddress
from .utils import cookieCart, cartData, guestOrder 

# Create your views here.


def index(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, "feggystreats/index.html", context)

def cookies(request):

    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']

    try:
        items = Items.objects.filter(category='cookie').all()
    except ObjectDoesNotExist:
        items = None


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "feggystreats/cookies.html", context)

def brownies(request):

    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']

    try:
        items = Items.objects.filter(category='brownie').all()
    except ObjectDoesNotExist:
        items = None


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "feggystreats/brownies.html", context)

def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "feggystreats/cart.html", context)

def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "feggystreats/checkout.html", context)

def addItem(request):
    data = json.loads(request.body)
    itemId = data.get("itemId", "")
    action = data.get("action", "")
    quantity = data.get("quantity", "")

    print(action)
    print(itemId)

    customer = request.user.customer
    item = Items.objects.get(pk=itemId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + int(quantity))
    if action == 'add2':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        customer, order = guestOrder(request, data)
        

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )

    print('data:', request.body)
    return JsonResponse('Payment Complete', safe=False)

def login_view(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "feggystreats/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        context = {'items':items, 'order':order, 'cartItems':cartItems}
        return render(request, "feggystreats/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "feggystreats/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, firstname, lastname, email, password)
            user.save()
        except IntegrityError:
            return render(request, "feggystreats/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {'items':items, 'order':order, 'cartItems':cartItems}
        return render(request, "feggystreats/register.html", context)

