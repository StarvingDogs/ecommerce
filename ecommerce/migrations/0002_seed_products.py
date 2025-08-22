from django.db import migrations
from faker import Faker

def seed_products(apps, schema_editor):
    Product = apps.get_model('ecommerce', 'Product')
    fake = Faker()
    categories = [fake.word() for _ in range(5)]
    brands = [fake.company() for _ in range(10)]
    products = []
    for i in range(1, 101):
        price = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=5.0, max_value=500.0), 2)
        stock = fake.random_int(min=1, max=200)
        products.append(Product(
            name=fake.unique.word().title() + f" {i}",
            brand=brands[i % 10],
            category=categories[i % 5],
            description=fake.text(max_nb_chars=100),
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
