from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from .models import User, Cart, Wishlist, Wallet, LoyaltyPoints

@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        # Create Cart
        Cart.objects.create(user=instance)
        
        # Create Wishlist (optional - many users prefer one wishlist)
        Wishlist.objects.create(user=instance)
        
        # Create Wallet
        Wallet.objects.create(user=instance)
        
        # Create Loyalty Points
        LoyaltyPoints.objects.create(user=instance)