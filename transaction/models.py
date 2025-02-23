from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Rent', 'Rent'),
        ('Salary', 'Salary'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Healthcare', 'Healthcare'),
        ('Other', 'Other'),
    ]

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def clean(self):
        if self.date is None:
            raise ValidationError({'date': 'Date is required.'})
        if self.date > timezone.now().date():
            raise ValidationError({'date': 'Date cannot be in the future.'})

        if self.transaction_type == 'income' and self.amount < 0:
            raise ValidationError({'amount': 'Income amount must be positive.'})
        elif self.transaction_type == 'expense' and self.amount > 0:
            raise ValidationError({'amount': 'Expense amount must be negative.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.description}"