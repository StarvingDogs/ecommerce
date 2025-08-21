from django.urls import path
from . import views

app_name = "ecommerce"
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increment/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('wishlists/', views.wishlist_list, name='wishlist_list'),
    path('wishlists/create/', views.wishlist_create, name='wishlist_create'),
    path('wishlists/<int:wishlist_id>/rename/', views.wishlist_rename, name='wishlist_rename'),
    path('wishlists/<int:wishlist_id>/delete/', views.wishlist_delete, name='wishlist_delete'),
    path('wishlists/<int:wishlist_id>/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlists/<int:wishlist_id>/remove/<int:item_id>/', views.wishlist_remove_item, name='wishlist_remove_item'),
    path('wishlists/<int:wishlist_id>/add_to_cart/<int:item_id>/', views.wishlist_add_to_cart, name='wishlist_add_to_cart'),
]
