from django import forms
import os
import stripe
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Customer, Order, OrderItem, Product, Cart, CartItem, Wishlist, WishlistItem
from django import forms
from .models import Review

class ExtendedUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=True, label='Address')
    phone = forms.CharField(max_length=20, required=True, label='Phone')


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            Customer.objects.create(user=user, address=address, phone=phone)
            messages.success(
                request, 'Registration successful. You can now log in.')
            return redirect('ecommerce:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'ecommerce/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('ecommerce:index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'ecommerce/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('ecommerce:index')


def index(request):
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    brands = Product.objects.values_list('brand', flat=True).distinct()

    selected_category = request.GET.get('category', '')
    selected_brand = request.GET.get('brand', '')
    search_query = request.GET.get('search', '')

    if selected_category:
        products = products.filter(category=selected_category)
    if selected_brand:
        products = products.filter(brand=selected_brand)
    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'search_query': search_query,
    }
    return render(request, 'ecommerce/index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    customer = None
    wishlists = None
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            wishlists = Wishlist.objects.filter(customer=customer)
    return render(request, 'ecommerce/detail.html', {'product': product, 'wishlists': wishlists})


@login_required
def add_to_wishlist(request, product_id):
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    wishlist_id = request.POST.get('wishlist_id')
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer=customer)
    # Prevent duplicates
    if not WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f'Added {product.name} to wishlist {wishlist.name}.')
    else:
        messages.info(request, f'{product.name} is already in wishlist {wishlist.name}.')
    return redirect('ecommerce:product_detail', pk=product_id)

def get_user_cart(request):
    if not request.user.is_authenticated:
        return None
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    return cart


@require_POST
def add_to_cart(request, product_id):
    cart = get_user_cart(request)
    if not cart:
        messages.error(request, 'You must be logged in to add items to cart.')
        return redirect('ecommerce:login')
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'Added {product.name} to cart.')
    # We can add to cart from the product detail page or the index page
    # Without this the user would be taken to the index page everytime
    # Let's use this to redirect back to whatever page the user was on (e.g from product detail page) else go back to the index page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('ecommerce:index')


@require_POST
def increment_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id,
                             cart__customer__user=request.user)
    item.quantity += 1
    item.save()
    messages.success(request, f'Increased quantity for {item.product.name}.')
    return redirect('ecommerce:view_cart')


@require_POST
def decrement_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id,
                             cart__customer__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.success(
            request, f'Decreased quantity for {item.product.name}.')
    else:
        item.delete()
        messages.success(request, f'Removed {item.product.name} from cart.')
    return redirect('ecommerce:view_cart')


@require_POST
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id,
                             cart__customer__user=request.user)
    item.delete()
    messages.success(request, f'Removed {item.product.name} from cart.')
    return redirect('ecommerce:view_cart')


def view_cart(request):
    cart = get_user_cart(request)
    items = cart.items.select_related('product') if cart else []
    subtotal = sum(item.product.price * item.quantity for item in items)
    return render(request, 'ecommerce/cart.html', {'cart': cart, 'items': items, 'subtotal': subtotal})

# Shipping info form


class ShippingInfoForm(forms.Form):
    address = forms.CharField(max_length=255, label='Address')
    city = forms.CharField(max_length=50, label='City')
    postal_code = forms.CharField(max_length=20, label='Postal Code')
    country = forms.CharField(max_length=50, label='Country')
    phone = forms.CharField(max_length=20, label='Phone')


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('ecommerce:login')
    cart = get_user_cart(request)
    items = cart.items.select_related('product') if cart else []
    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('ecommerce:view_cart')

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cart/'),
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Error creating Stripe session: {str(e)}')
        return redirect('ecommerce:checkout')

# Success and cancel views


def payment_success(request):
    if not request.user.is_authenticated:
        return redirect('ecommerce:login')
    customer = Customer.objects.get(user=request.user)
    cart = get_user_cart(request)
    items = cart.items.select_related('product') if cart else []
    if not items:
        messages.error(request, 'No items found for order.')
        return redirect('ecommerce:index')
    total = sum(item.product.price * item.quantity for item in items)
    # Create order
    order = Order.objects.create(
        customer=customer, total=total, status='Paid')
    for item in items:
        OrderItem.objects.create(
            order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    # Clear cart
    cart.items.all().delete()
    context = {
        'order': order,
    }
    return render(request, 'ecommerce/payment_success.html', context)


def payment_cancel(request):
    messages.info(request, 'You have cancelled the payment.')
    return redirect('ecommerce:view_cart')

# Order detail view
@login_required
def order_detail(request, order_id):
    customer = Customer.objects.get(user=request.user)
    order = get_object_or_404(customer.order_set, id=order_id)
    # For each product in the order, check if the user has already left a review
    review_status = []
    for item in order.items.select_related('product'):
        has_reviewed = item.product.reviews.filter(customer=customer).exists()
        review_status.append({'product_id': item.product.id, 'has_reviewed': has_reviewed})
    return render(request, 'ecommerce/order_detail.html', {'order': order, 'review_status': review_status})


# --- Review Form and View ---
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

@login_required
def leave_review(request, product_id, order_id):
    customer = Customer.objects.get(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    order = get_object_or_404(Order, pk=order_id, customer=customer)
    # Only allow review if not already reviewed
    if Review.objects.filter(product=product, customer=customer).exists():
        messages.info(request, 'You have already reviewed this product.')
        return redirect('ecommerce:order_detail', order_id=order_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = customer
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('ecommerce:order_detail', order_id=order_id)
    else:
        form = ReviewForm()
    return render(request, 'ecommerce/leave_review.html', {'form': form, 'product': product, 'order': order})
# Order history view


@login_required
def order_history(request):
    customer = Customer.objects.get(user=request.user)
    orders = customer.order_set.order_by('-created_at').prefetch_related('items__product')
    return render(request, 'ecommerce/order_history.html', {'orders': orders})

# --- Wishlist Management Views ---
@login_required
def wishlist_list(request):
    customer = get_object_or_404(Customer, user=request.user)
    wishlists = Wishlist.objects.filter(customer=customer)
    return render(request, 'ecommerce/wishlist_list.html', {'wishlists': wishlists})

@login_required
def wishlist_create(request):
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            wishlist = Wishlist.objects.create(customer=customer)
            wishlist.name = name
            wishlist.save()
            messages.success(request, f'Wishlist "{wishlist.name}" created successfully.')
            return redirect('ecommerce:wishlist_list')
        else:
            messages.error(request, 'Wishlist name cannot be empty.')
    return render(request, 'ecommerce/wishlist_create.html')

@login_required
def wishlist_rename(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer__user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            wishlist.name = name
            wishlist.save()
            messages.success(request, f'Wishlist renamed to "{wishlist.name}" successfully.')
            return redirect('ecommerce:wishlist_list')
        else:
            messages.error(request, 'Wishlist name cannot be empty.')
    return render(request, 'ecommerce/wishlist_rename.html', {'wishlist': wishlist})

@login_required
def wishlist_delete(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer__user=request.user)
    if request.method == 'POST':
        wishlist.delete()
        messages.success(request, f'Wishlist "{wishlist.name}" deleted successfully.')
        return redirect('ecommerce:wishlist_list')
    return render(request, 'ecommerce/wishlist_delete.html', {'wishlist': wishlist})


# --- Wishlist Detail and Item Actions ---
@login_required
def wishlist_detail(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer__user=request.user)
    items = wishlist.items.select_related('product')
    return render(request, 'ecommerce/wishlist_detail.html', {'wishlist': wishlist, 'items': items})

@login_required
def wishlist_remove_item(request, wishlist_id, item_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer__user=request.user)
    item = get_object_or_404(WishlistItem, id=item_id, wishlist=wishlist)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Item removed from wishlist.')
        return redirect('ecommerce:wishlist_detail', wishlist_id=wishlist.id)
    return redirect('ecommerce:wishlist_detail', wishlist_id=wishlist.id)

@login_required
def wishlist_add_to_cart(request, wishlist_id, item_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, customer__user=request.user)
    item = get_object_or_404(WishlistItem, id=item_id, wishlist=wishlist)
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    item.delete()
    messages.success(request, f'Item added to cart and removed from wishlist.')
    return redirect('ecommerce:wishlist_detail', wishlist_id=wishlist.id)