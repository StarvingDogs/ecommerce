from django.db import migrations

import random

def seed_products(apps, schema_editor):
    Product = apps.get_model('ecommerce', 'Product')
    products = []
    for i in range(1, 101):
        price = round(random.uniform(5.0, 500.0), 2)
        stock = random.randint(1, 200)
        products.append(Product(
            name=f'Product {i}',
            brand=f'Brand {i % 10}',
            category=f'Category {i % 5}',
            description=f'Sample description for product {i}.',
            price=price,
            stock=stock,
            image=''  # Leave blank for now
        ))
    Product.objects.bulk_create(products)

class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_products),
    ]
