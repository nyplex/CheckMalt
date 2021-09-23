from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'last_login', 'is_active')
    list_display_links = ('email', 'first_name')
    readonly_fields = ('email', 'last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ('first_name', 'last_name', 'email', 'last_login', 'is_active')
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
