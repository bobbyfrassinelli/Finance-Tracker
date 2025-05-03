import random
from datetime import timedelta, date
from django.utils.timezone import make_aware
from .models import Transaction, Person

def run():
    # Create people
    names = ['Bobby', 'Libby', 'Katie', 'Michael']
    people = []

    for name in names:
        person, created = Person.objects.get_or_create(name=name)
        people.append(person)

    # Create transactions
    today = date.today()
    for _ in range(30):
        person = random.choice(people)
        days_ago = random.randint(0, 88)
        t_date = today - timedelta(days=days_ago)
        t_type = random.choice(['Income', 'Expense'])
        amount = round(random.uniform(10, 500), 2)
        expenses = ['Gambling', 'Food', 'Gas', 'Entertainment', 'Video Games', 'Medical', 'Phone']
        incomes = ['Gambling', 'Work', 'Gifts']
        if t_type == 'Income':
            note = random.choice(incomes)
        else:
            note = random.choice(expenses)

        Transaction.objects.create(
            date=t_date,
            amount=amount,
            type=t_type,
            person=person,
            notes=note
        )
    print("✅ Dummy data loaded.")
