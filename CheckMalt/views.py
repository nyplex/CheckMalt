from store.models import Product
from django.shortcuts import render

def Home(request):
    products = Product.objects.all().filter(is_available=True)
    return render(request, 'home.html', {
        'products': products
    })