import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order

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
