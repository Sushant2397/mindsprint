from django.test import TestCase
from django.contrib.auth import get_user_model
from groups.models import Group, GroupMember
from expenses.models import Expense, ExpenseSplit
from .services import SettlementService
from decimal import Decimal

User = get_user_model()


class SettlementServiceTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com')
        self.user3 = User.objects.create_user(username='user3', email='user3@test.com')
        
        # Create test group
        self.group = Group.objects.create(
            name='Test Group',
            owner=self.user1,
            currency='INR'
        )
        
        # Add members
        GroupMember.objects.create(group=self.group, user=self.user1, role='owner')
        GroupMember.objects.create(group=self.group, user=self.user2, role='member')
        GroupMember.objects.create(group=self.group, user=self.user3, role='member')
        
        # Create test expenses
        self.expense1 = Expense.objects.create(
            group=self.group,
            payer=self.user1,
            amount_subtotal=Decimal('300.00'),
            amount_tax=Decimal('54.00'),
            vendor='Test Vendor 1',
            category='food'
        )
        
        self.expense2 = Expense.objects.create(
            group=self.group,
            payer=self.user2,
            amount_subtotal=Decimal('200.00'),
            amount_tax=Decimal('36.00'),
            vendor='Test Vendor 2',
            category='transport'
        )
        
        # Create equal splits
        for expense in [self.expense1, self.expense2]:
            amount_per_member = expense.total_amount / 3
            for user in [self.user1, self.user2, self.user3]:
                if user != expense.payer:
                    ExpenseSplit.objects.create(
                        expense=expense,
                        member=user,
                        amount_owed=amount_per_member,
                        split_type='equal'
                    )
    
    def test_compute_net_balances(self):
        service = SettlementService(self.group)
        balances = service.compute_net_balances()
        
        # User1 paid 354, owes 118 + 78.67 = 196.67, net = +157.33
        # User2 paid 236, owes 118 + 78.67 = 196.67, net = +39.33
        # User3 paid 0, owes 118 + 78.67 = 196.67, net = -196.67
        
        self.assertAlmostEqual(float(balances[self.user1.id]), 157.33, places=1)
        self.assertAlmostEqual(float(balances[self.user2.id]), 39.33, places=1)
        self.assertAlmostEqual(float(balances[self.user3.id]), -196.67, places=1)
    
    def test_greedy_netting(self):
        service = SettlementService(self.group)
        balances = service.compute_net_balances()
        transactions = service.greedy_netting(balances)
        
        # Should have transactions to settle the balances
        self.assertGreater(len(transactions), 0)
        
        # Check that total transaction amount equals total debt
        total_debt = sum(abs(amount) for amount in balances.values() if amount < 0)
        total_transactions = sum(t['amount'] for t in transactions)
        self.assertAlmostEqual(float(total_transactions), float(total_debt), places=1)
    
    def test_compute_settlement(self):
        service = SettlementService(self.group)
        settlement = service.compute_settlement('equal_split')
        
        self.assertIn('group_id', settlement)
        self.assertIn('transactions', settlement)
        self.assertIn('graph', settlement)
        self.assertEqual(settlement['group_id'], self.group.id)
        self.assertGreater(settlement['transaction_count'], 0)