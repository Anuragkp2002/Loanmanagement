from django.db import models
from django.contrib.auth.models import User

# Create your models here.








class LoanUser(models.Model):
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


class Loan(models.Model):
    STATUS_CHOICES = [("ACTIVE", "Active"), ("CLOSED", "Closed")]

    loan_id = models.CharField(max_length=20, unique=True,null=True)
    user = models.ForeignKey(LoanUser, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tenure = models.IntegerField(null=True)  # In months
    interest_rate = models.FloatField(null=True)  # Yearly Interest Rate
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)



class PaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, related_name='payment_schedule', on_delete=models.CASCADE,null=True)
    installment_no = models.PositiveIntegerField(null=True)
    due_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)

