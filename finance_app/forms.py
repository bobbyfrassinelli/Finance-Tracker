from django import forms
from datetime import date
from .models import Transaction, Person

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'type', 'person', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']


class ReportForm(forms.Form):
    MONTH_CHOICES = [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    current_year = date.today().year
    YEAR_CHOICES = [(y, str(y)) for y in range(current_year, current_year - 5, -1)]

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial=date.today().month,
        label="Month",
        required=False
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=current_year,
        label="Year",
        required=False
    )
