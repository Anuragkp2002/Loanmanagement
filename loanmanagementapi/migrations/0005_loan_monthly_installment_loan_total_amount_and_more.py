# Generated by Django 5.1.6 on 2025-03-18 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanmanagementapi', '0004_remove_loan_monthly_installment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='monthly_installment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='total_interest',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loanmanagementapi.user'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='tenure',
            field=models.IntegerField(null=True),
        ),
    ]
