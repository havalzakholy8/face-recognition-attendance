# tests/test_finance.py
import pytest
import os
from models.account_model import Account, CashAccount, BankAccount
from models.transaction_model import Transaction, ExpenseTransaction, IncomeTransaction
from models.budget_model import Budget
from managers.account_manager import AccountManager
from managers.transaction_manager import TransactionManager
from managers.budget_manager import BudgetManager
from exceptions import ValidationError, NotFoundError#, #StorageError

# Unit Tests - Testing individual components

def test_create_basic_account():
    """Test that we can create a basic account"""
    acc = Account("A1", "My Wallet", "cash", "HUF")
    assert acc.id == "A1"
    assert acc.name == "My Wallet"
    assert acc.account_type == "cash"
    assert acc.currency == "HUF"

def test_create_cash_account():
    """Test that CashAccount works correctly"""
    cash_acc = CashAccount("C1", "Wallet", "EUR")
    assert cash_acc.account_type == "cash"
    assert cash_acc.currency == "EUR"

def test_create_bank_account():
    """Test that BankAccount works correctly"""
    bank_acc = BankAccount("B1", "Savings", "USD")
    assert bank_acc.account_type == "bank"
    assert bank_acc.name == "Savings"

def test_account_without_id_raises_error():
    """Test that creating account without ID raises an error"""
    with pytest.raises(ValidationError):
        Account("", "No ID Account", "cash", "HUF")

def test_create_basic_transaction():
    """Test that we can create a basic transaction"""
    trans = Transaction("T1", "A1", "2024-11-01", 5000, "Groceries", "food")
    assert trans.id == "T1"
    assert trans.amount == 5000
    assert trans.category == "food"

def test_expense_transaction_makes_amount_negative():
    """Test that ExpenseTransaction automatically makes amount negative"""
    expense = ExpenseTransaction("E1", "A1", "2024-11-01", 3000, "Shopping", "clothes")
    assert expense.amount < 0

def test_income_transaction_makes_amount_positive():
    """Test that IncomeTransaction automatically makes amount positive"""
    income = IncomeTransaction("I1", "A1", "2024-11-01", -5000, "Salary", "work")
    assert income.amount > 0

def test_create_basic_budget():
    """Test that we can create a budget"""
    budget = Budget("B1", "2024-11", "food", 50000)
    assert budget.month == "2024-11"
    assert budget.category == "food"
    assert budget.limit_amount == 50000

def test_budget_with_negative_amount_raises_error():
    """Test that negative budget amount raises an error"""
    with pytest.raises(ValidationError):
        Budget("B1", "2024-11", "food", -1000)

# Integration Tests - Testing how components work together

def test_account_manager_can_create_account():
    """Test that AccountManager can create an account"""
    manager = AccountManager()
    manager.add_account("A1", "Test Account", "cash", "HUF")
    
    found_account = manager.find_account_by_id("A1")
    assert found_account.name == "Test Account"

def test_account_manager_prevents_duplicate_ids():
    """Test that AccountManager doesn't allow duplicate IDs"""
    manager = AccountManager()
    manager.add_account("A1", "First Account", "cash", "HUF")
    
    with pytest.raises(ValidationError):
        manager.add_account("A1", "Duplicate Account", "bank", "EUR")

def test_account_manager_can_update_account():
    """Test that we can update an existing account"""
    manager = AccountManager()
    manager.add_account("A1", "Old Name", "cash", "HUF")
    manager.modify_account("A1", name="New Name", currency="EUR")
    
    account = manager.find_account_by_id("A1")
    assert account.name == "New Name"
    assert account.currency == "EUR"

def test_account_manager_can_delete_account():
    """Test that we can delete an account"""
    manager = AccountManager()
    manager.add_account("A1", "To Be Deleted", "cash", "HUF")
    manager.remove_account("A1")
    
    with pytest.raises(NotFoundError):
        manager.find_account_by_id("A1")

def test_transaction_manager_crud_operations():
    """Test all basic transaction operations"""
    manager = TransactionManager()
    
    # Create
    manager.add_transaction("T1", "A1", "2024-11-01", 1000, "Test", "misc")
    assert len(manager.transactions) == 1
    
    # Update
    manager.modify_transaction("T1", amount=2000)
    trans = manager.find_transaction_by_id("T1")
    assert trans.amount == 2000
    
    # Delete
    manager.remove_transaction("T1")
    assert len(manager.transactions) == 0

def test_budget_manager_crud_operations():
    """Test all basic budget operations"""
    manager = BudgetManager()
    
    # Create
    manager.add_budget("B1", "2024-11", "food", 50000)
    assert len(manager.budgets) == 1
    
    # Find
    budget = manager.find_budget_by_id("B1")
    assert budget.category == "food"
    
    # Update
    manager.modify_budget("B1", limit_amount=60000)
    budget = manager.find_budget_by_id("B1")
    assert budget.limit_amount == 60000
    
    # Delete
    manager.remove_budget("B1")
    assert len(manager.budgets) == 0

# System Tests - Testing complete workflows

def test_complete_workflow_with_csv_files():
    """Test creating data, saving it, and loading it back"""
    # Setup
    acc_manager = AccountManager()
    acc_manager.filename = "test_accounts.csv"
    
    # Create some accounts
    acc_manager.add_account("A1", "Test Wallet", "cash", "HUF")
    acc_manager.add_account("A2", "Test Bank", "bank", "EUR")
    
    # Save to CSV
    acc_manager.save_to_file()
    
    # Create a new manager and load the data
    new_manager = AccountManager()
    new_manager.filename = "test_accounts.csv"
    new_manager.load_from_file()
    
    # Verify the data was loaded correctly
    assert len(new_manager.accounts) == 2
    account = new_manager.find_account_by_id("A1")
    assert account.name == "Test Wallet"
    
    # Clean up test file
    if os.path.exists("test_accounts.csv"):
        os.remove("test_accounts.csv")

def test_multiple_managers_working_together():
    """Test that different managers can work together"""
    acc_manager = AccountManager()
    trans_manager = TransactionManager()
    budget_manager = BudgetManager()
    
    # Create an account
    acc_manager.add_account("A1", "Main Account", "bank", "HUF")
    
    # Create a transaction for that account
    trans_manager.add_transaction("T1", "A1", "2024-11-01", 5000, "Shopping", "food")
    
    # Create a budget for the same category
    budget_manager.add_budget("B1", "2024-11", "food", 50000)
    
    # Verify everything exists
    assert len(acc_manager.accounts) == 1
    assert len(trans_manager.transactions) == 1
    assert len(budget_manager.budgets) == 1
    
    # Verify the relationships
    trans = trans_manager.find_transaction_by_id("T1")
    budget = budget_manager.find_budget_by_id("B1")
    assert trans.account_id == "A1"
    assert budget.category == "food"
