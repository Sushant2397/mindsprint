from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from groups.models import Group, GroupMember, FairnessPolicy
from expenses.models import Expense, ExpenseSplit
from payments.models import LedgerEntry
from datetime import datetime, timedelta
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for Shared Finance OS'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')
        
        # Create demo users
        users = self.create_demo_users()
        
        # Create demo groups
        groups = self.create_demo_groups(users)
        
        # Create demo expenses
        self.create_demo_expenses(groups)
        
        # Create demo fairness policies
        self.create_demo_fairness_policies(groups)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded demo data!')
        )
    
    def create_demo_users(self):
        """Create demo users"""
        users_data = [
            {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
            {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Smith'},
            {'username': 'charlie', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
            {'username': 'diana', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Wilson'},
            {'username': 'eve', 'email': 'eve@example.com', 'first_name': 'Eve', 'last_name': 'Davis'},
            {'username': 'frank', 'email': 'frank@example.com', 'first_name': 'Frank', 'last_name': 'Miller'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'phone': f'+91{random.randint(9000000000, 9999999999)}',
                    'kyc_status': 'verified' if random.choice([True, False]) else 'pending',
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
            users.append(user)
        
        self.stdout.write(f'Created {len(users)} demo users')
        return users
    
    def create_demo_groups(self, users):
        """Create demo groups"""
        groups_data = [
            {
                'name': 'Roommates - 2BHK Apartment',
                'description': 'Shared expenses for our 2BHK apartment',
                'group_type': 'roommates',
                'owner': users[0],
                'currency': 'INR',
                'members': [users[0], users[1], users[2]]
            },
            {
                'name': 'Society Committee',
                'description': 'Monthly society maintenance and events',
                'group_type': 'society',
                'owner': users[3],
                'currency': 'INR',
                'members': [users[3], users[4], users[5]]
            },
            {
                'name': 'Tech Club',
                'description': 'Technology club expenses and events',
                'group_type': 'club',
                'owner': users[1],
                'currency': 'INR',
                'members': [users[1], users[2], users[4], users[5]]
            }
        ]
        
        groups = []
        for group_data in groups_data:
            group, created = Group.objects.get_or_create(
                name=group_data['name'],
                defaults={
                    'description': group_data['description'],
                    'group_type': group_data['group_type'],
                    'owner': group_data['owner'],
                    'currency': group_data['currency'],
                    'settings': {
                        'auto_settle_threshold': 1000,
                        'notification_preferences': ['email', 'push']
                    }
                }
            )
            
            if created:
                # Add members
                for i, member in enumerate(group_data['members']):
                    role = 'owner' if member == group_data['owner'] else 'member'
                    GroupMember.objects.create(
                        group=group,
                        user=member,
                        role=role,
                        share_factor=Decimal('1.00'),
                        income_bracket=random.choice(['low', 'medium', 'high'])
                    )
            
            groups.append(group)
        
        self.stdout.write(f'Created {len(groups)} demo groups')
        return groups
    
    def create_demo_expenses(self, groups):
        """Create demo expenses"""
        categories = ['food', 'transport', 'utilities', 'entertainment', 'shopping']
        vendors = ['Swiggy', 'Uber', 'Electricity Board', 'Netflix', 'Amazon', 'Zomato', 'Ola']
        
        for group in groups:
            members = group.members.filter(is_active=True)
            if not members.exists():
                continue
            
            # Create 5-10 expenses per group
            num_expenses = random.randint(5, 10)
            for _ in range(num_expenses):
                payer = random.choice(members).user
                amount = Decimal(str(random.randint(100, 5000)))
                tax = amount * Decimal('0.18')  # 18% GST
                
                expense = Expense.objects.create(
                    group=group,
                    payer=payer,
                    amount_subtotal=amount,
                    amount_tax=tax,
                    vendor=random.choice(vendors),
                    category=random.choice(categories),
                    description=f'Demo expense for {group.name}',
                    date=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                
                # Create equal splits
                total_members = members.count()
                amount_per_member = expense.total_amount / total_members
                
                for member in members:
                    if member.user != payer:  # Payer doesn't owe themselves
                        ExpenseSplit.objects.create(
                            expense=expense,
                            member=member.user,
                            amount_owed=amount_per_member,
                            split_type='equal'
                        )
        
        self.stdout.write('Created demo expenses')
    
    def create_demo_fairness_policies(self, groups):
        """Create demo fairness policies"""
        policy_types = ['equal_split', 'income_based', 'custom_share']
        
        for group in groups:
            policy_type = random.choice(policy_types)
            FairnessPolicy.objects.create(
                group=group,
                policy_type=policy_type,
                parameters={
                    'description': f'Demo {policy_type} policy for {group.name}',
                    'auto_apply': False
                },
                created_by=group.owner
            )
        
        self.stdout.write('Created demo fairness policies')