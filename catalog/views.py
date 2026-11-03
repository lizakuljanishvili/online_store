from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count, Q
from decimal import Decimal, InvalidOperation

from .models import Product, Category
from .forms import ProductForm


def apply_product_filters(request, queryset,
                          use_category=True, use_sale=True):

    # Search
    search = request.GET.get('q', '').strip()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # Category filter
    if use_category:
        category_id = request.GET.get('category', '')

        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(category_id=category_id)
            except ValueError:
                pass

    # Sale filter
    if use_sale:
        sale = request.GET.get('sale', '')

        if sale == 'yes':
            queryset = queryset.filter(is_on_sale=True)

        elif sale == 'no':
            queryset = queryset.filter(is_on_sale=False)

    # Minimum price
    min_price = request.GET.get('min_price', '')

    if min_price:
        try:
            value = Decimal(min_price)

            if value.is_finite() and value >= 0:
                queryset = queryset.filter(price__gte=value)

        except InvalidOperation:
            pass

    # Maximum price
    max_price = request.GET.get('max_price', '')

    if max_price:
        try:
            value = Decimal(max_price)

            if value.is_finite() and value >= 0:
                queryset = queryset.filter(price__lte=value)

        except InvalidOperation:
            pass

    # Sorting
    sort = request.GET.get('sort', 'price_asc')

    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'newest': '-created_at',
    }

    queryset = queryset.order_by(
        sort_options.get(sort, 'price'),
        'pk'
    )

    return queryset


# HOME PAGE

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        return apply_product_filters(
            self.request,
            queryset
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)

        context['show_category_filter'] = True
        context['show_sale_filter'] = True

        return context


# CATEGORY PAGE

class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            pk=self.kwargs['pk']
        )

        queryset = Product.objects.filter(
            category=self.category,
            is_available=True
        )

        return apply_product_filters(
            self.request,
            queryset,
            use_category=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self.category
        context['show_category_filter'] = False
        context['show_sale_filter'] = True

        return context


# SALE PAGE

class SaleProductsView(ListView):
    model = Product
    template_name = 'catalog/sale_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_available=True,
            is_on_sale=True
        )

        return apply_product_filters(
            self.request,
            queryset,
            use_sale=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)

        context['show_category_filter'] = True
        context['show_sale_filter'] = False

        return context


# PRODUCT DETAIL PAGE

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


# ADD PRODUCT

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# UPDATE PRODUCT

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


# DELETE PRODUCT

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
