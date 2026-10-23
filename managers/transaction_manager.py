# managers/transaction_manager.py
from models.transaction_model import Transaction, ExpenseTransaction, IncomeTransaction
from storage.csv_storage import CSVStorage
from exceptions import NotFoundError, ValidationError

class TransactionManager:
    """Manages all transaction-related operations"""
    
    def __init__(self):
        self.transactions = []
        self.filename = "transactions.csv"
    
    def add_transaction(self, trans_id, account_id, date, amount, description, category, trans_type="normal"):
        """Creates a new transaction"""
        # Check if transaction ID already exists
        for t in self.transactions:
            if t.id == trans_id:
                raise ValidationError(f"Transaction ID {trans_id} already exists")
        
        # Create the appropriate transaction type
        if trans_type.lower() == "expense":
            new_transaction = ExpenseTransaction(trans_id, account_id, date, amount, description, category)
        elif trans_type.lower() == "income":
            new_transaction = IncomeTransaction(trans_id, account_id, date, amount, description, category)
        else:
            new_transaction = Transaction(trans_id, account_id, date, amount, description, category)
        
        self.transactions.append(new_transaction)
        print(f"Transaction created successfully: {new_transaction}")
        return new_transaction
    
    def show_all_transactions(self):
        """Displays all transactions"""
        if len(self.transactions) == 0:
            print("No transactions available.")
            return
        
        print("\n=== List of All Transactions ===")
        for trans in self.transactions:
            print(trans)
        print()
    
    def find_transaction_by_id(self, trans_id):
        """Finds and returns a transaction by its ID"""
        for trans in self.transactions:
            if trans.id == trans_id:
                return trans
        raise NotFoundError(f"Transaction ID {trans_id} not found")
    
    def modify_transaction(self, trans_id, amount=None, description=None, category=None):
        """Updates an existing transaction"""
        transaction = self.find_transaction_by_id(trans_id)
        
        if amount is not None:
            transaction.amount = float(amount)
        if description:
            transaction.description = description
        if category:
            transaction.category = category
        
        print(f"Transaction updated successfully: {transaction}")
        return transaction
    
    def remove_transaction(self, trans_id):
        """Deletes a transaction"""
        transaction = self.find_transaction_by_id(trans_id)
        self.transactions.remove(transaction)
        print(f"Transaction {trans_id} deleted successfully")
    
    def save_to_file(self):
        """Saves all transactions to CSV file"""
        transaction_data = []
        for trans in self.transactions:
            transaction_data.append(trans.to_dict())
        
        fieldnames = ['id', 'account_id', 'date', 'amount', 'description', 'category']
        CSVStorage.save_to_csv(self.filename, transaction_data, fieldnames)
    
    def load_from_file(self):
        """Loads transactions from CSV file"""
        data = CSVStorage.load_from_csv(self.filename)
        self.transactions = []
        
        for row in data:
            transaction = Transaction(
                row['id'],
                row['account_id'],
                row['date'],
                row['amount'],
                row['description'],
                row['category']
            )
            self.transactions.append(transaction)
