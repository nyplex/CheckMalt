from store.models import Product
from django.shortcuts import render

# Create your views here.

def store(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()
    return render(request, 'store/store.html', {
        'products': products,
        'product_count': product_count
    })