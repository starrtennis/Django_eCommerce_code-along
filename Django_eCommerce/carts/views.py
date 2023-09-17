    # navigation imports
from django.shortcuts import render, redirect, get_object_or_404

    # database/model object imports
from store.models import Product
from .models import Cart, CartItem

    # http-relevant import(s)
from django.http import HttpResponse

    # error-handling import(s)
from django.core.exceptions import ObjectDoesNotExist


    # filtered cart object
    # relevant variables calculated
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (7 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        print("You don't have money? What's wrong with you!")
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


    # the session key for the cart of the user/shopper
    # in one conveniently accessible variable
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


    # if no item of this type in cart yet, adds 1 to cart
    # otherwise, increments (increases by 1) quantity of the item in the cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 #cart_item.quantity = cart_item_quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')
    
    
    # decrements (reduces by 1) the quantity of an item in the user's cart
    # removes item outright if item quantity is only 1
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


    # removes item in user's cart outright
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
    
