from django.db import models
from django.contrib.auth.models import User

# Create your models here.





class Loan(models.Model):
    STATUS_CHOICES = [("ACTIVE", "Active"), ("CLOSED", "Closed")]

    loan_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # In months
    interest_rate = models.FloatField()  # Yearly Interest Rate
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    password = models.CharField(max_length=128,null=True)
    created_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    role = models.CharField(max_length=50,null=True)
    email = models.EmailField(unique=True,null=True)
    is_deleted = models.BooleanField(default=False,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    updated_at = models.DateTimeField(null=True)
