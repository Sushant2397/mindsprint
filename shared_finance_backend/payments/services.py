import uuid
from decimal import Decimal
from typing import Dict, Any
from django.conf import settings
from .models import Payment, LedgerEntry
import logging

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for handling payment flows"""
    
    @staticmethod
    def generate_upi_deeplink(amount: Decimal, payer_name: str, payee_name: str) -> str:
        """Generate mock UPI deep link URL"""
        # This is a mock implementation for demo purposes
        # In production, you'd integrate with real UPI providers
        payment_id = str(uuid.uuid4())[:8]
        return f"upi://pay?pa=demo@paytm&pn={payee_name}&am={amount}&cu=INR&tn=Shared Finance Payment {payment_id}"
    
    @staticmethod
    def initiate_payment(ledger_entry: LedgerEntry, method: str) -> Dict[str, Any]:
        """Initiate a payment"""
        payment = Payment.objects.create(
            ledger_entry=ledger_entry,
            method=method,
            amount=ledger_entry.amount,
            status='pending'
        )
        
        response_data = {
            'payment_id': payment.id,
            'amount': float(payment.amount),
            'method': payment.method,
            'status': payment.status,
            'created_at': payment.created_at
        }
        
        if method == 'UPI_DEEPLINK':
            upi_link = PaymentService.generate_upi_deeplink(
                payment.amount,
                ledger_entry.from_member.username,
                ledger_entry.to_member.username
            )
            payment.upi_deeplink = upi_link
            payment.save()
            response_data['upi_deeplink'] = upi_link
        
        return response_data
    
    @staticmethod
    def process_webhook(webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment webhook"""
        payment_id = webhook_data.get('payment_id')
        status = webhook_data.get('status')
        transaction_id = webhook_data.get('transaction_id')
        
        if not payment_id or not status:
            return {'error': 'Invalid webhook data'}
        
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.webhook_data = webhook_data
            payment.payment_ref = transaction_id or payment.payment_ref
            
            if status == 'success':
                payment.status = 'completed'
                # Update ledger entry
                payment.ledger_entry.status = 'paid'
                payment.ledger_entry.save()
            elif status == 'failed':
                payment.status = 'failed'
            else:
                payment.status = 'processing'
            
            payment.save()
            
            return {
                'payment_id': payment.id,
                'status': payment.status,
                'message': f'Payment {status}'
            }
            
        except Payment.DoesNotExist:
            return {'error': 'Payment not found'}
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {'error': 'Internal server error'}
    
    @staticmethod
    def get_payment_status(payment_id: int) -> Dict[str, Any]:
        """Get payment status"""
        try:
            payment = Payment.objects.get(id=payment_id)
            return {
                'payment_id': payment.id,
                'status': payment.status,
                'amount': float(payment.amount),
                'method': payment.method,
                'created_at': payment.created_at,
                'updated_at': payment.updated_at
            }
        except Payment.DoesNotExist:
            return {'error': 'Payment not found'}


class UPIWebhookSimulator:
    """Simulator for UPI webhook responses (for demo purposes)"""
    
    @staticmethod
    def simulate_webhook(payment_id: int, success: bool = True) -> Dict[str, Any]:
        """Simulate a UPI webhook response"""
        if success:
            return {
                'payment_id': payment_id,
                'status': 'success',
                'transaction_id': f'TXN{payment_id}{uuid.uuid4().hex[:8].upper()}',
                'timestamp': '2024-01-01T12:00:00Z',
                'gateway_response': 'Transaction successful'
            }
        else:
            return {
                'payment_id': payment_id,
                'status': 'failed',
                'error_code': 'INSUFFICIENT_FUNDS',
                'error_message': 'Insufficient funds in account',
                'timestamp': '2024-01-01T12:00:00Z'
            }