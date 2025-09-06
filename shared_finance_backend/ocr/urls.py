from django.urls import path
from . import views

urlpatterns = [
    path('expenses/<int:expense_id>/upload_receipt/', views.upload_receipt, name='upload-receipt'),
]