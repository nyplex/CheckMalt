from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from cart.models import Cart, CartItem
from store.models import Product
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.get(product=product, cart=cart)

    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()

    return redirect('cart')


def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.get(product=product, cart=cart)
    cart_items.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += round((item.product.price * item.quantity), 2)
            quantity += item.quantity
        tax = round((12 * total) / 100, 2)
        grand_total = format(total + tax, '.2f')
    except ObjectDoesNotExist:
        pass

    return render(request, 'store/cart.html', {
        'total': total,
        'quantity': quantity,
        'items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    })
