from django.contrib import admin

from .models import Person, Transaction

admin.site.register(Person)
admin.site.register(Transaction)