# models/account.py
from exceptions import ValidationError

class Account:
    """Basic account class"""
    
    def __init__(self, account_id, name, account_type, currency):
        # Check if required fields are provided
        if not account_id or not name:
            raise ValidationError("Account ID and name cannot be empty")
        
        self.id = account_id
        self.name = name
        self.account_type = account_type
        self.currency = currency
    
    def to_dict(self):
        """Returns account data as a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'currency': self.currency
        }
    
    def __str__(self):
        return f"{self.id} - {self.name} ({self.account_type}, {self.currency})"


class CashAccount(Account):
    """Represents a cash wallet"""
    
    def __init__(self, account_id, name, currency):
        super().__init__(account_id, name, "cash", currency)


class BankAccount(Account):
    """Represents a bank account"""
    
    def __init__(self, account_id, name, currency):
        super().__init__(account_id, name, "bank", currency)
