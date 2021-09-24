from django.contrib import admin
from django.db import models
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)