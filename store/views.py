from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from . models import *
from .utils import cookieCart,cartData,guestOrder

# Create your views here.


def store(request):
    # print(request.user.customer)

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products,'cartItems':cartItems}

    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        # customer = request.user.customer
        order, created = Order.objects.get_or_create(complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def main(request):
    context = {}
    return render(request, 'store/main.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem.set_all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    # data = cartData(request)
    # cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item added to the cart', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(complete=False)
    else:
        customer,order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = request.user,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted',safe=False)