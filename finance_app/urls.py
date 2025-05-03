from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('delete-transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('edit-transaction/<int:pk>/', views.edit_transaction, name='edit_transaction'),
]
