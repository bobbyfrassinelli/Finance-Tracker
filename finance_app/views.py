from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta, date
from django.db import connection
from .models import Transaction, Person
from .forms import TransactionForm, PersonForm, ReportForm

def transaction_list(request):
    filter_type = request.GET.get('filter_type')
    filter_note = request.GET.get('filter_note')
    filter_person = request.GET.get('filter_person')

    transactions = Transaction.objects.all().order_by('-date')

    if filter_type in ['Income', 'Expense']:
        transactions = transactions.filter(type=filter_type)

    if filter_note:
        transactions = transactions.filter(notes=filter_note)

    if filter_person:
        transactions = transactions.filter(person__id=filter_person)

    distinct_notes = Transaction.objects.values_list('notes', flat=True).distinct()
    distinct_people = Person.objects.filter(transaction__isnull=False).distinct()

    people = Person.objects.all()
    transaction_form = TransactionForm()
    person_form = PersonForm()
    report_form = ReportForm(request.GET or None)

    report_data = []
    totals = {'income': 0, 'expense': 0, 'net': 0}

    if request.method == 'POST':
        if 'submit_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction_form.save()
                return redirect('transaction_list')
        elif 'submit_person' in request.POST:
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                person_form.save()
                return redirect('transaction_list')

    if (
        'month' in request.GET and request.GET.get('month') and
        'year' in request.GET and request.GET.get('year') and
        report_form.is_valid()
    ):
        month = int(report_form.cleaned_data['month'])
        year = int(report_form.cleaned_data['year'])

        start_date = date(year, month, 1)
        end_date = (
            date(year + 1, 1, 1) - timedelta(days=1)
            if month == 12 else date(year, month + 1, 1) - timedelta(days=1)
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.date, p.name, t.type, t.amount, t.notes
                FROM finance_app_transaction t
                LEFT JOIN finance_app_person p ON t.person_id = p.id
                WHERE t.date BETWEEN %s AND %s
                ORDER BY t.date ASC
            """, [start_date, end_date])

            rows = cursor.fetchall()

        for row in rows:
            t_date, person, t_type, amount, notes = row
            report_data.append({
                'date': t_date,
                'person': person,
                'type': t_type,
                'amount': amount,
                'notes': notes
            })

            if t_type == 'Income':
                totals['income'] += float(amount)
            else:
                totals['expense'] += float(amount)

        totals['net'] = totals['income'] - totals['expense']

    return render(request, 'transaction_list.html', {
        'transactions': transactions,
        'people': people,
        'transaction_form': transaction_form,
        'person_form': person_form,
        'report_form': report_form,
        'report_data': report_data,
        'totals': totals,
        'filter_type': filter_type,
        'filter_note': filter_note,
        'filter_person': filter_person,
        'distinct_notes': distinct_notes,
        'distinct_people': distinct_people,
    })

def delete_transaction(request, pk):
    Transaction.objects.filter(pk=pk).delete()
    return redirect('transaction_list')

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})
