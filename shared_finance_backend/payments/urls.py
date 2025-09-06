from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ledger', views.LedgerEntryViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('initiate/', views.initiate_payment, name='initiate-payment'),
    path('webhook/', views.payment_webhook, name='payment-webhook'),
    path('status/<int:payment_id>/', views.payment_status, name='payment-status'),
    path('simulate/<int:payment_id>/', views.simulate_webhook, name='simulate-webhook'),
]