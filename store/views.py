from django.core import paginator
from cart.models import CartItem
from category.models import Category
from store.models import Product
from django.shortcuts import get_object_or_404, render
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(is_available=True, category=category)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    return render(request, 'store/store.html', {
        'products': paged_product,
        'product_count': product_count
    })

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    return render(request, 'store/product_detail.html', {
        'product': product,
        'in_cart': in_cart
    })