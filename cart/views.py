from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.shortcuts import get_object_or_404, redirect, render
import collections

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        #print(request.POST)
        for item in request.POST:
            #print(item)
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variations_category__iexact=key, variations_value__iexact=value)
                product_variation.append(variation)
                #print(product_variation)
            except:
                pass
        print(product_variation)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        print(cart_item)
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        #print(existing_variation_list)
        #print(product_variation)

        if product_variation in existing_variation_list:
            index = existing_variation_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_items = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
    except:
        pass
    return redirect('cart')


def delete_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
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
