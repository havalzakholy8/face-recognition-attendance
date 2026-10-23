# managers/account_manager.py
from models.account_model import Account, CashAccount, BankAccount
from storage.csv_storage import CSVStorage
from exceptions import NotFoundError, ValidationError

class AccountManager:
    """Manages all account-related operations"""
    
    def __init__(self):
        self.accounts = []
        self.filename = "accounts.csv"
    
    def add_account(self, account_id, name, account_type, currency):
        """Creates a new account"""
        # Check if account ID already exists
        for acc in self.accounts:
            if acc.id == account_id:
                raise ValidationError(f"Account ID {account_id} already exists")
        
        # Create the appropriate account type
        if account_type.lower() == "cash":
            new_account = CashAccount(account_id, name, currency)
        elif account_type.lower() == "bank":
            new_account = BankAccount(account_id, name, currency)
        else:
            new_account = Account(account_id, name, account_type, currency)
        
        self.accounts.append(new_account)
        print(f"Account created successfully: {new_account}")
        return new_account
    
    def show_all_accounts(self):
        """Displays all accounts"""
        if len(self.accounts) == 0:
            print("No accounts available.")
            return
        
        print("\n=== List of All Accounts ===")
        for acc in self.accounts:
            print(acc)
        print()
    
    def find_account_by_id(self, account_id):
        """Finds and returns an account by its ID"""
        for acc in self.accounts:
            if acc.id == account_id:
                return acc
        raise NotFoundError(f"Account ID {account_id} not found")
    
    def modify_account(self, account_id, name=None, currency=None):
        """Updates an existing account"""
        account = self.find_account_by_id(account_id)
        
        if name:
            account.name = name
        if currency:
            account.currency = currency
        
        print(f"Account updated successfully: {account}")
        return account
    
    def remove_account(self, account_id):
        """Deletes an account"""
        account = self.find_account_by_id(account_id)
        self.accounts.remove(account)
        print(f"Account {account_id} deleted successfully")
    
    def save_to_file(self):
        """Saves all accounts to CSV file"""
        account_data = []
        for acc in self.accounts:
            account_data.append(acc.to_dict())
        
        fieldnames = ['id', 'name', 'account_type', 'currency']
        CSVStorage.save_to_csv(self.filename, account_data, fieldnames)
    
    def load_from_file(self):
        """Loads accounts from CSV file"""
        data = CSVStorage.load_from_csv(self.filename)
        self.accounts = []
        
        for row in data:
            acc_type = row['account_type']
            if acc_type == 'cash':
                account = CashAccount(row['id'], row['name'], row['currency'])
            elif acc_type == 'bank':
                account = BankAccount(row['id'], row['name'], row['currency'])
            else:
                account = Account(row['id'], row['name'], acc_type, row['currency'])
            self.accounts.append(account)
