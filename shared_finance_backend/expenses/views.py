from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Expense, ExpenseSplit
from .serializers import ExpenseSerializer, ExpenseSplitSerializer, ExpenseCreateSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for Expense model"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Expense.objects.filter(
            group__members__user=self.request.user,
            group__members__is_active=True
        ).select_related('payer', 'group').prefetch_related('splits__member')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        expense = serializer.save()
        
        # Create equal splits for all group members
        group = expense.group
        members = group.members.filter(is_active=True)
        total_members = members.count()
        
        if total_members > 0:
            amount_per_member = expense.total_amount / total_members
            
            for member in members:
                ExpenseSplit.objects.create(
                    expense=expense,
                    member=member.user,
                    amount_owed=amount_per_member,
                    split_type='equal'
                )
    
    @action(detail=True, methods=['post'])
    def mark_settled(self, request, pk=None):
        """Mark expense as settled"""
        expense = self.get_object()
        
        # Check if user is payer or group member
        if expense.payer != request.user and not expense.group.members.filter(user=request.user).exists():
            return Response(
                {'error': 'You are not authorized to modify this expense'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        expense.is_settled = True
        expense.save()
        
        return Response({'message': 'Expense marked as settled'})
    
    @action(detail=True, methods=['get'])
    def splits(self, request, pk=None):
        """Get expense splits"""
        expense = self.get_object()
        splits = expense.splits.all()
        serializer = ExpenseSplitSerializer(splits, many=True)
        return Response(serializer.data)


class ExpenseSplitViewSet(viewsets.ModelViewSet):
    """ViewSet for ExpenseSplit model"""
    queryset = ExpenseSplit.objects.all()
    serializer_class = ExpenseSplitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ExpenseSplit.objects.filter(
            expense__group__members__user=self.request.user,
            expense__group__members__is_active=True
        ).select_related('expense', 'member')
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark split as paid"""
        split = self.get_object()
        
        # Check if user is the member who owes this amount
        if split.member != request.user:
            return Response(
                {'error': 'You can only mark your own splits as paid'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        split.is_paid = True
        split.save()
        
        return Response({'message': 'Split marked as paid'})