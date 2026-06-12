import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Category, Product, ProductVariant, 
    Cart, CartItem, Wishlist, Order, Address
)
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# ====================== PUBLIC PAGES ======================

def home(request):
    context = {
        'categories': Category.objects.filter(is_active=True)[:12],
        'featured_products': Product.objects.filter(is_active=True)[:8],
    }
    return render(request, 'store/index.html', context)


def shop(request, category_slug=None):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    categories = Category.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        current_category = category
    else:
        current_category = None

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)


# ====================== CART & WISHLIST ======================


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'addresses': addresses,
    }
    return render(request, 'store/profile.html', context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {'orders': orders}
    return render(request, 'store/my_orders.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'store/order_detail.html', context)



@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('variant__product', 'variant__product__brand')
    
    total = sum(item.variant.price * item.quantity for item in items)
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')   # ← This forces login
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        variant=variant,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{variant.product.name} added to cart!")
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('variant__product')
    context = {'wishlist_items': items}
    return render(request, 'store/wishlist.html', context)


@login_required(login_url='login')   # ← This forces login
def add_to_wishlist(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    Wishlist.objects.get_or_create(user=request.user, variant=variant)
    messages.success(request, "Added to wishlist!")
    return redirect('wishlist')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'store/register.html', context)


# ====================== CHECKOUT ======================

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('variant__product')
    total_amount = sum(item.variant.price * item.quantity for item in items)

    if total_amount <= 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    try:
        # Create Razorpay Order
        razorpay_order = razorpay_client.order.create({
            'amount': int(total_amount * 100),  # in paise
            'currency': 'INR',
            'payment_capture': '1'
        })

        context = {
            'items': items,
            'total': total_amount,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount': int(total_amount * 100),
        }
        return render(request, 'store/checkout.html', context)

    except Exception as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('cart')




@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify signature (optional but recommended)
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            
            # Create Order in Database
            cart = Cart.objects.get(user=request.user)
            total = sum(item.variant.price * item.quantity for item in cart.items.all())

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                final_amount=total,
                status='confirmed',
                payment_method='razorpay',
                payment_status='paid',
                tracking_number=f"GP{int(total)}{request.user.id}"
            )

            # Move cart items to order
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price
                )

            # Clear cart
            cart.items.all().delete()

            return render(request, 'store/payment_success.html', {'order': order})

        except:
            return render(request, 'store/payment_failed.html')

    return redirect('checkout')