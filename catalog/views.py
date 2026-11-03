from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count

from .models import Product, Category
from .forms import ProductForm


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
        ).filter(product_count__gt=0)

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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def product_update(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'catalog/product_form.html',
        {'form': form, 'product': product}
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        product.delete()
        return redirect('home')

    return render(
        request,
        'catalog/product_confirm_delete.html',
        {'product': product}
    )