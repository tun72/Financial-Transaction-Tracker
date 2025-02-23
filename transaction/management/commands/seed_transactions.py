from django.core.management.base import BaseCommand
from transaction.models import Transaction
from django.utils import timezone
from decimal import Decimal
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with transactions.'

    def handle(self, *args, **options):
        categories = [choice[0] for choice in Transaction.CATEGORY_CHOICES]
        start_date = timezone.now().date() - timezone.timedelta(days=365)

        for _ in range(200):
            transaction_type = random.choice(['income', 'expense'])
            amount = Decimal(random.randint(100, 10000)) / 100  # $1.00 to $100.00
            if transaction_type == 'expense':
                amount = -amount

            Transaction.objects.create(
                amount=amount,
                date=fake.date_between(start_date=start_date, end_date='today'),
                category=random.choice(categories),
                transaction_type=transaction_type,
                description=fake.sentence(),
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded 200 transactions.'))