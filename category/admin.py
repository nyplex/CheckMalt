from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = ('name', 'description')
    list_display_links = ('name',)
    list_filter = ('name',)

admin.site.register(Category, CategoryAdmin)
