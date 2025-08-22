
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	def __str__(self):
		return self.user.username


class Product(models.Model):
	name = models.CharField(max_length=100)
	brand = models.CharField(max_length=50)
	category = models.CharField(max_length=50)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	image = models.ImageField(upload_to='products/', blank=True, null=True)
	def __str__(self):
		return self.name


class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f"Cart {self.id} for {self.customer.user.username}"


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	def __str__(self):
		return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, default='Pending')
	def __str__(self):
		return f"Order {self.id} by {self.customer.user.username}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	def __str__(self):
		return f"{self.quantity} x {self.product.name}"


class Wishlist(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name if self.name else f"Wishlist {self.id} for {self.customer.user.username}"


class WishlistItem(models.Model):
	wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.product.name


class ShippingInfo(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=50)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	def __str__(self):
		return f"Shipping for Order {self.order.id}"


class Review(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(default=1)
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.rating} stars by {self.customer.user.username} for Order {self.order.id}"
