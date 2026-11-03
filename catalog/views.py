from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Product, Category


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            is_available=True
        ).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(
            product_count__gt=0
        )

        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            pk=self.kwargs['pk']
        )

        return Product.objects.filter(
            category=self.category,
            is_available=True
        ).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SaleProductsView(ListView):
    model = Product
    template_name = 'catalog/sale_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            is_available=True,
            is_on_sale=True
        ).order_by('price')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)