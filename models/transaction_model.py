# models/transaction.py
from exceptions import ValidationError

class Transaction:
    """Basic transaction class"""
    
    def __init__(self, trans_id, account_id, date, amount, description, category):
        # Validate required fields
        if not trans_id or not account_id:
            raise ValidationError("Transaction ID and Account ID are required")
        
        # Make sure amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            raise ValidationError("Amount must be a valid number")
        
        self.id = trans_id
        self.account_id = account_id
        self.date = date
        self.amount = amount
        self.description = description
        self.category = category
    
    def to_dict(self):
        """Returns transaction data as a dictionary"""
        return {
            'id': self.id,
            'account_id': self.account_id,
            'date': self.date,
            'amount': self.amount,
            'description': self.description,
            'category': self.category
        }
    
    def __str__(self):
        return f"{self.id} - {self.date}: {self.amount} ({self.description}) - {self.category}"


class ExpenseTransaction(Transaction):
    """Represents money going out (expenses)"""
    
    def __init__(self, trans_id, account_id, date, amount, description, category):
        # Convert amount to negative for expenses
        if float(amount) > 0:
            amount = -abs(float(amount))
        super().__init__(trans_id, account_id, date, amount, description, category)


class IncomeTransaction(Transaction):
    """Represents money coming in (income)"""
    
    def __init__(self, trans_id, account_id, date, amount, description, category):
        # Convert amount to positive for income
        amount = abs(float(amount))
        super().__init__(trans_id, account_id, date, amount, description, category)
