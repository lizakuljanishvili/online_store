from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path(
        'category/<int:pk>/',
        views.CategoryProductsView.as_view(),
        name='category_products'
    ),

    path(
        'sale/',
        views.SaleProductsView.as_view(),
        name='sale_products'
    ),

    path(
        'product/<int:pk>/',
        views.ProductDetailView.as_view(),
        name='product_detail'
    ),

    path(
        'product/add/',
        views.ProductCreateView.as_view(),
        name='product_add'
    ),

    path(
        'product/<int:pk>/update/',
        views.product_update,
        name='product_update'
    ),

    path(
        'product/<int:pk>/delete/',
        views.product_delete,
        name='product_delete'
    ),
]