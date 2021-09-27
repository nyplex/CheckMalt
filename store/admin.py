from django.contrib import admin
from django.db import models
from .models import Product, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variations_category', 'variations_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variations_category', 'variations_value', 'is_active')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
