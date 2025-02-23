from django import forms
from .models import Transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            raise forms.ValidationError("Date is required.")
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')



        # Ensure amount is not None before performing operations
        if transaction_type and amount is not None:
            if transaction_type == 'expense':
                cleaned_data['amount'] = -abs(amount)  # Ensure amount is negative for expenses
            elif transaction_type == 'income':
                cleaned_data['amount'] = abs(amount)  # Ensure amount is positive for income

        return cleaned_data