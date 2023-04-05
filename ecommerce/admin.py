from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from . models import *


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 0 

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug', 'total_products']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):

    list_display = ['name','slug', 'price', 'stock', 'is_available']
    list_editable = ['price', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInLine]

@admin.register(Banner)
class AdminBanner(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'get_image']
    list_editable = ['is_active']

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />'.format(obj.image.url))
        else:
            return "No Image"

@admin.register(Settings)
class AdminSetting(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'address'] 
    list_editable = ['email', 'phone', 'address']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'city', 'total', 'status']
    list_filter = ['status']
    list_editable = ['status']