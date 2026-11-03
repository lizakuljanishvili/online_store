from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'description',
            'price',
            'category',
            'image',
            'is_available',
            'is_on_sale',
        ]