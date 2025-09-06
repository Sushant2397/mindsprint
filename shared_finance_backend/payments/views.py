from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment, LedgerEntry
from .serializers import PaymentSerializer, LedgerEntrySerializer, PaymentCreateSerializer
from .services import PaymentService, UPIWebhookSimulator


class LedgerEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for LedgerEntry model"""
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LedgerEntry.objects.filter(
            from_member=self.request.user
        ).select_related('from_member', 'to_member', 'ref_expense')


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment model"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(
            ledger_entry__from_member=self.request.user
        ).select_related('ledger_entry__from_member', 'ledger_entry__to_member')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get payment status"""
        payment = self.get_object()
        result = PaymentService.get_payment_status(payment.id)
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def simulate_webhook(self, request, pk=None):
        """Simulate webhook for demo purposes"""
        payment = self.get_object()
        success = request.data.get('success', True)
        
        webhook_data = UPIWebhookSimulator.simulate_webhook(payment.id, success)
        result = PaymentService.process_webhook(webhook_data)
        
        return Response(result)


# Function-based views for additional endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """Initiate a payment"""
    
    ledger_entry_id = request.data.get('ledger_entry_id')
    method = request.data.get('method', 'UPI_DEEPLINK')
    
    if not ledger_entry_id:
        return Response(
            {'error': 'ledger_entry_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate payment method
    valid_methods = [choice[0] for choice in Payment.PAYMENT_METHODS]
    if method not in valid_methods:
        return Response(
            {'error': f'Invalid payment method. Must be one of: {valid_methods}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ledger_entry = get_object_or_404(LedgerEntry, id=ledger_entry_id)
        
        # Check if user is involved in this ledger entry
        if ledger_entry.from_member != request.user and ledger_entry.to_member != request.user:
            return Response(
                {'error': 'You are not authorized to initiate this payment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if payment is already pending or completed
        existing_payment = Payment.objects.filter(
            ledger_entry=ledger_entry,
            status__in=['pending', 'processing', 'completed']
        ).first()
        
        if existing_payment:
            return Response(
                {'error': 'Payment already exists for this ledger entry'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initiate payment
        payment_data = PaymentService.initiate_payment(ledger_entry, method)
        
        return Response(payment_data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': f'Error initiating payment: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_webhook(request):
    """Handle payment webhook (simulated)"""
    webhook_data = request.data
    
    try:
        result = PaymentService.process_webhook(webhook_data)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result)
    
    except Exception as e:
        return Response(
            {'error': f'Error processing webhook: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request, payment_id):
    """Get payment status"""
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        
        # Check if user is involved in this payment
        if (payment.ledger_entry.from_member != request.user and 
            payment.ledger_entry.to_member != request.user):
            return Response(
                {'error': 'You are not authorized to view this payment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        result = PaymentService.get_payment_status(payment_id)
        return Response(result)
    
    except Exception as e:
        return Response(
            {'error': f'Error getting payment status: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simulate_webhook(request, payment_id):
    """Simulate webhook for demo purposes"""
    success = request.data.get('success', True)
    
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        
        # Check if user is involved in this payment
        if (payment.ledger_entry.from_member != request.user and 
            payment.ledger_entry.to_member != request.user):
            return Response(
                {'error': 'You are not authorized to simulate this payment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Simulate webhook
        webhook_data = UPIWebhookSimulator.simulate_webhook(payment_id, success)
        result = PaymentService.process_webhook(webhook_data)
        
        return Response(result)
    
    except Exception as e:
        return Response(
            {'error': f'Error simulating webhook: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )