from category.models import Category
from store.models import Product
from django.shortcuts import get_object_or_404, render

# Create your views here.

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(is_available=True, category=category)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    return render(request, 'store/store.html', {
        'products': products,
        'product_count': product_count
    })