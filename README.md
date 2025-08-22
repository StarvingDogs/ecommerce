# Project Architecture

This Django eCommerce project is organized as follows:

- **ecommerce/**: Main app containing models, views, templates, and URLs for the eCommerce functionality.
- **cinema/**: Additional app (purpose to be documented if relevant).
- **mysite/**: Project configuration, settings, and root URLs.
- **templates/**: HTML templates using Bootstrap for UI.
- **db.sqlite3**: SQLite database for development.
- **manage.py**: Django management script.

## Features

This project implements the following eCommerce features:

- **Customer Registration & Authentication**: Users can register, log in, and log out securely.
- **Product Catalogue**: Browse products with pagination, view item details.
- **Search & Filter**: Search by brand, item name, or category.
- **Shopping Cart**: Add, increment, decrement, and remove items from the cart.
- **Shipping Information**: Enter and manage shipping details during checkout.
- **Stripe Payment Integration**: Secure payment processing using Stripe.
- **Order Management**: View order details, order history, and delete orders.
- **Wishlist**: Create, view, rename, and delete wishlists; add/remove items; add to cart from wishlist.
- **Product Reviews & Ratings**: Leave reviews and star ratings for products.

See below for server run instructions and environment setup.

## Run Server

`STRIPE_SECRET_KEY='your stripe secret key' STRIPE_PUBLISHABLE_KEY='your stripe publishable key' python manage.py runserver;`
