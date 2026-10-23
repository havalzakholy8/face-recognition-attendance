# managers/budget_manager.py
from models.budget_model import Budget
from storage.csv_storage import CSVStorage
from exceptions import NotFoundError, ValidationError

class BudgetManager:
    """Manages all budget-related operations"""
    
    def __init__(self):
        self.budgets = []
        self.filename = "budgets.csv"
    
    def add_budget(self, budget_id, month, category, limit_amount):
        """Creates a new budget"""
        # Check if budget ID already exists
        for b in self.budgets:
            if b.id == budget_id:
                raise ValidationError(f"Budget ID {budget_id} already exists")
        
        new_budget = Budget(budget_id, month, category, limit_amount)
        self.budgets.append(new_budget)
        print(f"Budget created successfully: {new_budget}")
        return new_budget
    
    def show_all_budgets(self):
        """Displays all budgets"""
        if len(self.budgets) == 0:
            print("No budgets available.")
            return
        
        print("\n=== List of All Budgets ===")
        for budget in self.budgets:
            print(budget)
        print()
    
    def find_budget_by_id(self, budget_id):
        """Finds and returns a budget by its ID"""
        for budget in self.budgets:
            if budget.id == budget_id:
                return budget
        raise NotFoundError(f"Budget ID {budget_id} not found")
    
    def modify_budget(self, budget_id, month=None, category=None, limit_amount=None):
        """Updates an existing budget"""
        budget = self.find_budget_by_id(budget_id)
        
        if month:
            budget.month = month
        if category:
            budget.category = category
        if limit_amount is not None:
            budget.limit_amount = float(limit_amount)
        
        print(f"Budget updated successfully: {budget}")
        return budget
    
    def remove_budget(self, budget_id):
        """Deletes a budget"""
        budget = self.find_budget_by_id(budget_id)
        self.budgets.remove(budget)
        print(f"Budget {budget_id} deleted successfully")
    
    def save_to_file(self):
        """Saves all budgets to CSV file"""
        budget_data = []
        for budget in self.budgets:
            budget_data.append(budget.to_dict())
        
        fieldnames = ['id', 'month', 'category', 'limit_amount']
        CSVStorage.save_to_csv(self.filename, budget_data, fieldnames)
    
    def load_from_file(self):
        """Loads budgets from CSV file"""
        data = CSVStorage.load_from_csv(self.filename)
        self.budgets = []
        
        for row in data:
            budget = Budget(
                row['id'],
                row['month'],
                row['category'],
                row['limit_amount']
            )
            self.budgets.append(budget)
