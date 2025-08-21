from django import forms
from django.views.decorators.http import require_POST
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Customer, Product, Cart, CartItem


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
    return render(request, 'ecommerce/detail.html', {'product': product})


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


def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to checkout.')
        return redirect('ecommerce:login')
    customer = Customer.objects.get(user=request.user)
    cart = get_user_cart(request)
    items = cart.items.select_related('product') if cart else []
    if not items:
        messages.error(
            request, 'Your cart is empty. Add items before checking out.')
        return redirect('ecommerce:view_cart')
    subtotal = sum(item.product.price * item.quantity for item in items)

    initial = {
        'address': customer.address,
        'phone': customer.phone,
    }
    form = ShippingInfoForm(request.POST or None, initial=initial)
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'address': customer.address,
        'phone': customer.phone,
    }
    if request.method == 'POST' and form.is_valid():
        # Save shipping info and proceed to payment (not implemented yet)
        shipping_data = form.cleaned_data
        messages.success(
            request, 'Shipping info submitted. Proceed to payment.')
        # Redirect to payment or order confirmation page
        return redirect('ecommerce:view_cart')
    return render(request, 'ecommerce/checkout.html', {
        'user_info': user_info,
        'form': form,
        'items': items,
        'subtotal': subtotal,
    })
