from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'category',
        'is_available',
        'is_on_sale'
    )

    list_filter = ('category', 'is_available', 'is_on_sale')
    search_fields = ('name',)