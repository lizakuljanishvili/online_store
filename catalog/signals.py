from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_save, sender=Product)
def product_updated(sender, instance, created, **kwargs):

    if not created:
        print(f'Product "{instance.name}" was updated.')