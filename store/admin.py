from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    User, Address, Category, SubCategory, Brand, Product, 
    ProductVariant, ProductImage, Cart, CartItem, Wishlist,
    Order, OrderItem, Payment, Review, Coupon, Banner,
    Vendor, Inventory, ReturnRefund, Transaction, 
    Wallet, LoyaltyPoints
)


# ====================== BASIC MODELS ======================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_vendor', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'phone']
    list_filter = ['is_vendor', 'is_staff', 'is_active']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'pincode', 'is_default']
    list_filter = ['is_default', 'city', 'state']
    search_fields = ['full_name', 'phone']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discount_price', 'is_active']
    list_filter = ['is_active', 'category', 'brand']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'sku', 'price', 'stock']
    list_filter = ['is_active']
    search_fields = ['sku', 'product__name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']


# ====================== CART & WISHLIST ======================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'variant', 'quantity', 'added_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'variant', 'added_at']


# ====================== ORDER & PAYMENT ======================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_status', 'final_amount', 'order_date']
    list_filter = ['status', 'payment_status']
    search_fields = ['id', 'user__username']
    date_hierarchy = 'order_date'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'variant', 'quantity', 'price']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_id', 'amount', 'status', 'payment_date']
    list_filter = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['comment']


# ====================== ADVANCED MODELS ======================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'discount_amount', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'is_approved', 'created_at']
    list_filter = ['is_approved']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['variant', 'stock', 'low_stock_threshold']


@admin.register(ReturnRefund)
class ReturnRefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'requested_at']
    list_filter = ['status']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'timestamp']
    list_filter = ['transaction_type']


# ====================== VERY ADVANCED ======================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'points']