# models/budget.py
from exceptions import ValidationError

class Budget:
    """Represents a monthly budget for a category"""
    
    def __init__(self, budget_id, month, category, limit_amount):
        # Check that all fields are provided
        if not budget_id or not month or not category:
            raise ValidationError("Budget ID, month, and category are required")
        
        # Validate the limit amount
        try:
            limit_amount = float(limit_amount)
            if limit_amount <= 0:
                raise ValidationError("Budget limit must be greater than zero")
        except ValueError:
            raise ValidationError("Budget limit must be a valid number")
        
        self.id = budget_id
        self.month = month
        self.category = category
        self.limit_amount = limit_amount
    
    def to_dict(self):
        """Returns budget data as a dictionary"""
        return {
            'id': self.id,
            'month': self.month,
            'category': self.category,
            'limit_amount': self.limit_amount
        }
    
    def __str__(self):
        return f"{self.id} - {self.month} | {self.category}: {self.limit_amount}"
