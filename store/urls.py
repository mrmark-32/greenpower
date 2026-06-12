from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/', views.shop, name='shop_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart & Wishlist
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:variant_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # Account Section
    path('accounts/login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
]