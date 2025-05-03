from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
        ]


