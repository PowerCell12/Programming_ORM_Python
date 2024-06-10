import os
from decimal import Decimal

import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product

#Create and run your queries within functions

def get_profiles(search_string=None):

    if search_string is None:
            return ""


    query = Q(full_name__icontains=f'{search_string}') | Q(email__icontains=f'{search_string}') | Q(phone_number__icontains=f'{search_string}')
    all_profiles = Profile.objects.filter(query).order_by('full_name')
    list1 = []

    if not all_profiles:
        return ""

    for profile1 in all_profiles:
        num_of_orders = Order.objects.filter(profile=profile1).count()
        list1.append(f"Profile: {profile1.full_name}, email: {profile1.email}, phone number: {profile1.phone_number}, orders: {num_of_orders}")

    return '\n'.join(list1)


def get_loyal_profiles():
    all_profiles = Profile.objects.get_regular_customers()

    if not all_profiles:
        return ""

    list1 = []

    for thing in all_profiles:
        num_of_orders = Order.objects.filter(profile=thing).count()
        list1.append(f"Profile: {thing.full_name}, orders: {num_of_orders}")

    return '\n'.join(list1)


def get_last_sold_products():
    last_order = Order.objects.order_by('products__name').last()

    if not last_order:
        return ""
    list1 = []

    for thing in last_order.products.values():
        list1.append(thing['name'])

    return f"Last sold products: {', '.join(list1)}"


## from here
def get_top_products():
    most_sold = Product.objects.annotate(most_sold_count=Count('order')).filter(most_sold_count__gt=0).order_by('-most_sold_count', 'name')

    if not most_sold:
        return ""

    list1 = []
    count = 0

    list1.append(f"Top products:")

    for sold in most_sold:
        count += 1

        list1.append(f"{sold.name}, sold {sold.most_sold_count} times")

        if count == 5:
            break

    return '\n'.join(list1)



def apply_discounts():
    query = Q(is_completed=False) & Q(products_count__gt=2)
    orders = Order.objects.annotate(products_count=Count('products')).filter(query)

    for order in orders:
        order.total_price = order.total_price * Decimal(0.9)
        order.save()

    return f"Discount applied to {len(orders)} orders."



def complete_order():
    order = Order.objects.order_by("creation_date").filter(is_completed=False).first()

    if not order:
        return ""

    order.is_completed = True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    return "Order has been completed!"


# def products():
#     Product.objects.create(name="Product1", price=100, in_stock=10, is_available=True)
#     Product.objects.create(name="Product2", price=200, in_stock=20, is_available=True)
#     Product.objects.create(name="Product3", price=300, in_stock=30, is_available=True)
#     Product.objects.create(name="Product4", price=400, in_stock=40, is_available=True)
#     Product.objects.create(name="Product5", price=500, in_stock=50, is_available=True)
#     Product.objects.create(name="Product6", price=600, in_stock=60, is_available=True)
#     Product.objects.create(name="Product7", price=700, in_stock=70, is_available=True)
#
#
#     Profile.objects.create(full_name="Profile1", email="p1@p1.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile2", email="p2@p2.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile3", email="p3@p3.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile4", email="p4@p4.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile5", email="p5@p5.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile6", email="p6@p6.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#     Profile.objects.create(full_name="Profile7", email="p7@p7.com", phone_number="123-456-7890", address="123 Main St", is_active=True)
#
#
#     first = Order.objects.create(profile=Profile.objects.get(full_name="Profile1"), total_price=1000, is_completed=False)
#     second = Order.objects.create(profile=Profile.objects.get(full_name="Profile2"), total_price=2000, is_completed=False)
#     third = Order.objects.create(profile=Profile.objects.get(full_name="Profile3"), total_price=3000, is_completed=False)
#
#     first.products.add(Product.objects.get(name="Product1"))
#     first.products.add(Product.objects.get(name="Product2"))
#     first.products.add(Product.objects.get(name="Product3"))
#     second.products.add(Product.objects.get(name="Product4"))
#     second.products.add(Product.objects.get(name="Product5"))
#     third.products.add(Product.objects.get(name="Product6"))
#     third.products.add(Product.objects.get(name="Product7"))

print(get_top_products())