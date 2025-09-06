from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from groups.models import Group
from .services import SettlementService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def compute_settlement(request, group_id):
    """Compute settlement for a group"""
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user is a member of the group
    if not group.members.filter(user=request.user, is_active=True).exists():
        return Response(
            {'error': 'You are not a member of this group'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    policy_type = request.data.get('policy_type', 'equal_split')
    
    # Validate policy type
    valid_policies = ['equal_split', 'income_based', 'custom_share', 'proportional']
    if policy_type not in valid_policies:
        return Response(
            {'error': f'Invalid policy type. Must be one of: {valid_policies}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        settlement_service = SettlementService(group)
        settlement = settlement_service.compute_settlement(policy_type)
        
        return Response(settlement)
    
    except Exception as e:
        return Response(
            {'error': f'Error computing settlement: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_settlement_graph(request, group_id):
    """Get settlement graph for a group"""
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user is a member of the group
    if not group.members.filter(user=request.user, is_active=True).exists():
        return Response(
            {'error': 'You are not a member of this group'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        settlement_service = SettlementService(group)
        balances = settlement_service.compute_net_balances()
        transactions = settlement_service.greedy_netting(balances)
        graph = settlement_service.create_settlement_graph(transactions)
        
        return Response({
            'group_id': group.id,
            'group_name': group.name,
            'graph': graph,
            'member_balances': {
                str(user_id): float(amount) 
                for user_id, amount in balances.items()
            }
        })
    
    except Exception as e:
        return Response(
            {'error': f'Error generating settlement graph: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )