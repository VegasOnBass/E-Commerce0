import json

from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'cart_items' :0, 'cart_total' :0}
    cartItems = order['cart_total']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            item = Items.objects.get(id=i)
            total = (item.price * cart[i]['quantity'])

            order['cart_items'] += cart[i]['quantity']
            order['cart_total'] += total 

            item = {
                'item':{
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'imageURL': item.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order, 'cartItems':cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request, data):
    print('User not logged in.')

    print('Cookies:', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    for i in items:
        item = Items.objects.get(id=i['item']['id'])

        orderItem = OrderItem.objects.create(
            item = item,
            order = order,
            quantity = i['quantity']
        )
    return customer, order