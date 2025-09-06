import networkx as nx
from decimal import Decimal
from collections import defaultdict
from typing import List, Dict, Tuple, Any
from groups.models import Group, GroupMember
from expenses.models import Expense, ExpenseSplit
from payments.models import LedgerEntry
import logging

logger = logging.getLogger(__name__)


class SettlementService:
    """Service for computing fair settlements using networkx"""
    
    def __init__(self, group: Group):
        self.group = group
        self.members = list(group.members.filter(is_active=True).select_related('user'))
        self.member_ids = [member.user.id for member in self.members]
    
    def compute_net_balances(self) -> Dict[int, Decimal]:
        """Compute net balance for each member (positive = owed money, negative = owes money)"""
        balances = defaultdict(Decimal)
        
        # Get all expenses and their splits
        expenses = Expense.objects.filter(
            group=self.group,
            is_settled=False
        ).prefetch_related('splits')
        
        for expense in expenses:
            # Add what the payer paid
            balances[expense.payer.id] += expense.total_amount
            
            # Subtract what each member owes
            for split in expense.splits.all():
                balances[split.member.id] -= split.amount_owed
        
        return dict(balances)
    
    def greedy_netting(self, balances: Dict[int, Decimal]) -> List[Dict[str, Any]]:
        """Greedy netting algorithm to minimize transactions"""
        # Separate debtors and creditors
        debtors = [(user_id, abs(amount)) for user_id, amount in balances.items() if amount < 0]
        creditors = [(user_id, amount) for user_id, amount in balances.items() if amount > 0]
        
        # Sort by amount (largest first)
        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)
        
        transactions = []
        debtor_idx = 0
        creditor_idx = 0
        
        while debtor_idx < len(debtors) and creditor_idx < len(creditors):
            debtor_id, debt_amount = debtors[debtor_idx]
            creditor_id, credit_amount = creditors[creditor_idx]
            
            # Calculate transaction amount
            transaction_amount = min(debt_amount, credit_amount)
            
            if transaction_amount > 0:
                transactions.append({
                    'from_member': debtor_id,
                    'to_member': creditor_id,
                    'amount': transaction_amount,
                    'explanation': f"Debt settlement of ₹{transaction_amount}"
                })
                
                # Update remaining amounts
                debtors[debtor_idx] = (debtor_id, debt_amount - transaction_amount)
                creditors[creditor_idx] = (creditor_id, credit_amount - transaction_amount)
            
            # Move to next debtor or creditor if current one is settled
            if debtors[debtor_idx][1] == 0:
                debtor_idx += 1
            if creditors[creditor_idx][1] == 0:
                creditor_idx += 1
        
        return transactions
    
    def create_settlement_graph(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a networkx graph representation of the settlement"""
        G = nx.DiGraph()
        
        # Add nodes (members)
        for member in self.members:
            G.add_node(member.user.id, 
                      username=member.user.username,
                      role=member.role)
        
        # Add edges (transactions)
        for transaction in transactions:
            G.add_edge(
                transaction['from_member'],
                transaction['to_member'],
                amount=transaction['amount'],
                explanation=transaction['explanation']
            )
        
        return {
            'nodes': [
                {
                    'id': node,
                    'username': data['username'],
                    'role': data['role']
                }
                for node, data in G.nodes(data=True)
            ],
            'edges': [
                {
                    'from': edge[0],
                    'to': edge[1],
                    'amount': data['amount'],
                    'explanation': data['explanation']
                }
                for edge, data in G.edges(data=True)
            ]
        }
    
    def compute_settlement(self, policy_type: str = 'equal_split') -> Dict[str, Any]:
        """Compute settlement based on fairness policy"""
        try:
            # Get net balances
            balances = self.compute_net_balances()
            
            # Apply fairness policy
            if policy_type == 'income_based':
                balances = self._apply_income_based_policy(balances)
            elif policy_type == 'custom_share':
                balances = self._apply_custom_share_policy(balances)
            # For equal_split and proportional, use current balances as-is
            
            # Compute transactions using greedy netting
            transactions = self.greedy_netting(balances)
            
            # Create settlement graph
            graph = self.create_settlement_graph(transactions)
            
            # Calculate total settlement amount
            total_amount = sum(t['amount'] for t in transactions)
            
            return {
                'group_id': self.group.id,
                'group_name': self.group.name,
                'policy_type': policy_type,
                'total_settlement_amount': float(total_amount),
                'transaction_count': len(transactions),
                'transactions': transactions,
                'graph': graph,
                'member_balances': {
                    str(user_id): float(amount) 
                    for user_id, amount in balances.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Error computing settlement: {e}")
            raise
    
    def _apply_income_based_policy(self, balances: Dict[int, Decimal]) -> Dict[int, Decimal]:
        """Apply income-based fairness policy"""
        # This is a simplified implementation
        # In a real system, you'd have more sophisticated income-based calculations
        adjusted_balances = {}
        
        for user_id, amount in balances.items():
            member = next((m for m in self.members if m.user.id == user_id), None)
            if member and member.income_bracket == 'low':
                # Reduce debt for low-income members
                adjusted_balances[user_id] = amount * Decimal('0.8')
            else:
                adjusted_balances[user_id] = amount
        
        return adjusted_balances
    
    def _apply_custom_share_policy(self, balances: Dict[int, Decimal]) -> Dict[int, Decimal]:
        """Apply custom share factor policy"""
        adjusted_balances = {}
        
        for user_id, amount in balances.items():
            member = next((m for m in self.members if m.user.id == user_id), None)
            if member:
                # Adjust based on share factor
                adjusted_balances[user_id] = amount * member.share_factor
            else:
                adjusted_balances[user_id] = amount
        
        return adjusted_balances


# ILP Solver stub (for future implementation)
class ILPSettlementService:
    """Integer Linear Programming settlement service (placeholder)"""
    
    def __init__(self, group: Group):
        self.group = group
    
    def compute_optimal_settlement(self, balances: Dict[int, Decimal]) -> List[Dict[str, Any]]:
        """
        Compute optimal settlement using ILP solver.
        This is a placeholder for future implementation with OR-Tools or similar.
        """
        # TODO: Implement ILP solver for provably minimal transactions
        # This would use libraries like OR-Tools, PuLP, or CVXPY
        logger.info("ILP settlement not yet implemented, falling back to greedy algorithm")
        return []