from django.views.generic import ListView, CreateView
from django.db.models import Sum, Min, Max
from .models import Transaction
from .forms import TransactionForm
from django.urls import reverse_lazy
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from openpyxl import Workbook
from .models import Transaction

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset.order_by('-date')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = context['transactions']

        # Financial Summaries
        total_income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = abs(
            transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0)
        net_balance = total_income - total_expenses

        # Average Monthly Expense
        dates = Transaction.objects.aggregate(min_date=Min('date'), max_date=Max('date'))
        start_date = dates['min_date']
        end_date = dates['max_date']
        months_count = 0

        if start_date and end_date:
            delta = relativedelta(end_date, start_date)
            months_count = delta.years * 12 + delta.months + 1  # Inclusive

        average_monthly_expense = total_expenses / months_count if months_count else 0

        context.update({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'average_monthly_expense': average_monthly_expense,
            'categories': Transaction.CATEGORY_CHOICES,
        })
        return context




def export_transactions_excel(request):
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"

    # Add headers to the worksheet
    headers = ["Id", "Date", "Description", "Amount", "Category", "Type"]
    ws.append(headers)

    # Fetch transactions based on filters (if any)
    transactions = Transaction.objects.all()

    # Apply filters if they exist in the request
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        transactions = transactions.filter(category=category)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Add transaction data to the worksheet
    for transaction in transactions:
        ws.append([
            transaction.id,
            transaction.date.strftime("%Y-%m-%d"),
            transaction.description,
            transaction.amount,
            transaction.get_category_display(),
            transaction.get_transaction_type_display(),
        ])

    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transactions.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    # success_url = reverse_lazy('transaction_list')
