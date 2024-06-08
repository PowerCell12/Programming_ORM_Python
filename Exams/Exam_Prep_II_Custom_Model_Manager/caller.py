import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# from main_app.models import Profile, Order
#Create and run your queries within functions

# def create():
#     Profile.objects.create(
#         full_name='John Doe',
#         email='pKqoG@example.com',
#         phone_number='123-456-7890',
#         address='123 Main St',
#         is_active=True,
#         creation_date='2022-01-01')
#     Profile.objects.create(full_name='Jane Doe', email='pKqoG@example.com', phone_number='123-456-7890', address='123 Main St', is_active=True, creation_date='2022-01-01')
#     Profile.objects.create(full_name='John Smith', email='pKqoG@example.com', phone_number='123-456-7890', address='123 Main St', is_active=True, creation_date='2022-01-01')
#
#     Order.objects.create(profile=Profile.objects.get(full_name='John Doe'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='John Doe'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='John Doe'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#
#
#     Order.objects.create(profile=Profile.objects.get(full_name='Jane Doe'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='Jane Doe'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#
#     Order.objects.create(profile=Profile.objects.get(full_name='John Smith'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='John Smith'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='John Smith'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#     Order.objects.create(profile=Profile.objects.get(full_name='John Smith'), total_price=100.00, creation_date='2022-01-01', is_completed=True)
#
#
# for things in Profile.objects.get_regular_customers():
#     print(things.full_name)