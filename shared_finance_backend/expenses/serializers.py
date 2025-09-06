from rest_framework import serializers
from .models import Expense, ExpenseSplit
from groups.serializers import GroupSerializer
from users.serializers import UserSerializer


class ExpenseSplitSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    member_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ExpenseSplit
        fields = ['id', 'member', 'member_id', 'amount_owed', 'split_type',
                 'metadata', 'is_paid', 'created_at']
        read_only_fields = ['id', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    payer = UserSerializer(read_only=True)
    payer_id = serializers.IntegerField(write_only=True)
    group = GroupSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True)
    splits = ExpenseSplitSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = Expense
        fields = ['id', 'group', 'group_id', 'payer', 'payer_id', 'amount_subtotal',
                 'amount_tax', 'total_amount', 'vendor', 'gstin', 'invoice_no',
                 'category', 'description', 'date', 'receipt_file', 'ocr_data',
                 'is_settled', 'created_at', 'updated_at', 'splits']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['group_id', 'payer_id', 'amount_subtotal', 'amount_tax',
                 'vendor', 'gstin', 'invoice_no', 'category', 'description', 'date']
    
    def create(self, validated_data):
        expense = Expense.objects.create(**validated_data)
        
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
        
        return expense