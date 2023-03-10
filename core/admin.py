from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('email', 'first_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
