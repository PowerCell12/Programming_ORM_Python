from datetime import date
from django.db import models

CITIES = [
    ('Sofia', 'Sofia'),
    ('Plovdiv', 'Plovdiv'),
    ('Burgas', 'Burgas'),
    ('Varna', 'Varna'),
]


class Employee(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    photo = models.URLField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    works_full_time = models.BooleanField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Department(models.Model):
    code = models.CharField(max_length=4, primary_key=True, unique=True, blank=True)
    name = models.CharField(max_length=50, unique=True, blank=True)
    employees_count = models.IntegerField("Employees Count", default=1)
    location = models.CharField(max_length=20, blank=True, null=True, choices=CITIES)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    duration_in_days = models.PositiveIntegerField("Duration in Days", blank=True, null=True)
    estimated_hours = models.FloatField("Estimated Hours", blank=True, null=True)
    start_date = models.DateField("Start Date", blank=True, null=True, default=date.today)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)