from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import uuid
from .models import Consent


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_consent(request):
    """Create a consent for data sharing (Account Aggregator simulation)"""
    purpose = request.data.get('purpose')
    audience = request.data.get('audience')
    scope = request.data.get('scope', {})
    expires_in_days = request.data.get('expires_in_days', 30)
    
    if not purpose or not audience:
        return Response(
            {'error': 'purpose and audience are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate purpose
    valid_purposes = [choice[0] for choice in Consent.PURPOSES]
    if purpose not in valid_purposes:
        return Response(
            {'error': f'Invalid purpose. Must be one of: {valid_purposes}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate audience
    valid_audiences = [choice[0] for choice in Consent.AUDIENCES]
    if audience not in valid_audiences:
        return Response(
            {'error': f'Invalid audience. Must be one of: {valid_audiences}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Generate consent token
        consent_token = f"CONSENT_{uuid.uuid4().hex.upper()}"
        
        # Calculate expiry
        expires_at = timezone.now() + timedelta(days=expires_in_days)
        
        # Create consent
        consent = Consent.objects.create(
            user=request.user,
            purpose=purpose,
            audience=audience,
            scope=scope,
            consent_token=consent_token,
            expires_at=expires_at
        )
        
        return Response({
            'consent_id': consent.id,
            'consent_token': consent_token,
            'purpose': purpose,
            'audience': audience,
            'scope': scope,
            'expires_at': expires_at,
            'created_at': consent.created_at
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': f'Error creating consent: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_consent(request, consent_id):
    """Get consent details"""
    consent = get_object_or_404(Consent, id=consent_id, user=request.user)
    
    return Response({
        'consent_id': consent.id,
        'consent_token': consent.consent_token,
        'purpose': consent.purpose,
        'audience': consent.audience,
        'scope': consent.scope,
        'is_active': consent.is_active,
        'expires_at': consent.expires_at,
        'created_at': consent.created_at
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_data(request, consent_id):
    """Simulate data sharing based on consent"""
    consent = get_object_or_404(Consent, id=consent_id, user=request.user)
    
    if not consent.is_active:
        return Response(
            {'error': 'Consent is not active'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if consent.expires_at < timezone.now():
        return Response(
            {'error': 'Consent has expired'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Simulate data sharing based on purpose and scope
        shared_data = simulate_data_sharing(consent)
        
        return Response({
            'consent_id': consent.id,
            'consent_token': consent.consent_token,
            'shared_data': shared_data,
            'shared_at': timezone.now()
        })
    
    except Exception as e:
        return Response(
            {'error': f'Error sharing data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_consent(request, consent_id):
    """Revoke a consent"""
    consent = get_object_or_404(Consent, id=consent_id, user=request.user)
    
    consent.is_active = False
    consent.save()
    
    return Response({
        'message': 'Consent revoked successfully',
        'consent_id': consent.id
    })


def simulate_data_sharing(consent):
    """Simulate data sharing based on consent purpose and scope"""
    # This is a mock implementation for demo purposes
    # In production, you'd implement actual data sharing logic
    
    shared_data = {
        'user_id': consent.user.id,
        'username': consent.user.username,
        'purpose': consent.purpose,
        'audience': consent.audience,
        'scope': consent.scope
    }
    
    if consent.purpose == 'expense_analysis':
        shared_data['expense_data'] = {
            'total_expenses': 15000.00,
            'category_breakdown': {
                'food': 5000.00,
                'transport': 3000.00,
                'utilities': 2000.00,
                'entertainment': 5000.00
            },
            'monthly_trend': [1200, 1500, 1800, 2000]
        }
    
    elif consent.purpose == 'settlement_calculation':
        shared_data['settlement_data'] = {
            'outstanding_balance': 2500.00,
            'pending_payments': 3,
            'settlement_history': [
                {'date': '2024-01-01', 'amount': 500.00, 'status': 'completed'},
                {'date': '2024-01-15', 'amount': 750.00, 'status': 'pending'}
            ]
        }
    
    elif consent.purpose == 'group_insights':
        shared_data['group_data'] = {
            'group_count': 3,
            'active_groups': ['Roommates', 'Society Committee'],
            'total_shared_expenses': 45000.00,
            'settlement_efficiency': 0.85
        }
    
    return shared_data