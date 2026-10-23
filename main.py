# main.py
from managers.account_manager import AccountManager
from managers.transaction_manager import TransactionManager
from managers.budget_manager import BudgetManager
from exceptions import FinanceError

def display_main_menu():
    """Shows the main menu options"""
    print("\n" + "="*40)
    print("   PERSONAL FINANCE MANAGER")
    print("="*40)
    print("1. Manage Accounts")
    print("2. Manage Transactions")
    print("3. Manage Budgets")
    print("4. Save All Data to CSV")
    print("5. Load All Data from CSV")
    print("6. Exit")
    print("="*40)

def display_account_menu():
    """Shows the account menu options"""
    print("\n--- Account Management ---")
    print("1. View All Accounts")
    print("2. Add New Account")
    print("3. Modify Account")
    print("4. Remove Account")
    print("5. Return to Main Menu")

def display_transaction_menu():
    """Shows the transaction menu options"""
    print("\n--- Transaction Management ---")
    print("1. View All Transactions")
    print("2. Add New Transaction")
    print("3. Modify Transaction")
    print("4. Remove Transaction")
    print("5. Return to Main Menu")

def display_budget_menu():
    """Shows the budget menu options"""
    print("\n--- Budget Management ---")
    print("1. View All Budgets")
    print("2. Add New Budget")
    print("3. Modify Budget")
    print("4. Remove Budget")
    print("5. Return to Main Menu")

def manage_accounts(account_manager):
    """Handles all account-related operations"""
    while True:
        display_account_menu()
        user_choice = input("Select an option: ").strip()
        
        try:
            if user_choice == "1":
                account_manager.show_all_accounts()
            
            elif user_choice == "2":
                acc_id = input("Enter Account ID: ").strip()
                acc_name = input("Enter Account Name: ").strip()
                acc_type = input("Enter Account Type (cash/bank): ").strip()
                acc_currency = input("Enter Currency (HUF/EUR/USD): ").strip()
                account_manager.add_account(acc_id, acc_name, acc_type, acc_currency)
            
            elif user_choice == "3":
                acc_id = input("Enter Account ID to modify: ").strip()
                new_name = input("Enter new name (press Enter to skip): ").strip()
                new_currency = input("Enter new currency (press Enter to skip): ").strip()
                account_manager.modify_account(
                    acc_id,
                    name=new_name if new_name else None,
                    currency=new_currency if new_currency else None
                )
            
            elif user_choice == "4":
                acc_id = input("Enter Account ID to remove: ").strip()
                confirmation = input(f"Are you sure you want to delete {acc_id}? (yes/no): ").strip()
                if confirmation.lower() == "yes":
                    account_manager.remove_account(acc_id)
            
            elif user_choice == "5":
                break
            
            else:
                print("Invalid option. Please try again.")
        
        except FinanceError as error:
            print(f"Error: {error}")

def manage_transactions(transaction_manager):
    """Handles all transaction-related operations"""
    while True:
        display_transaction_menu()
        user_choice = input("Select an option: ").strip()
        
        try:
            if user_choice == "1":
                transaction_manager.show_all_transactions()
            
            elif user_choice == "2":
                trans_id = input("Enter Transaction ID: ").strip()
                acc_id = input("Enter Account ID: ").strip()
                trans_date = input("Enter Date (YYYY-MM-DD): ").strip()
                trans_amount = input("Enter Amount: ").strip()
                trans_desc = input("Enter Description: ").strip()
                trans_category = input("Enter Category: ").strip()
                trans_type = input("Enter Type (expense/income/normal): ").strip()
                transaction_manager.add_transaction(trans_id, acc_id, trans_date, trans_amount, trans_desc, trans_category, trans_type)
            
            elif user_choice == "3":
                trans_id = input("Enter Transaction ID to modify: ").strip()
                new_amount = input("Enter new amount (press Enter to skip): ").strip()
                new_desc = input("Enter new description (press Enter to skip): ").strip()
                new_category = input("Enter new category (press Enter to skip): ").strip()
                transaction_manager.modify_transaction(
                    trans_id,
                    amount=float(new_amount) if new_amount else None,
                    description=new_desc if new_desc else None,
                    category=new_category if new_category else None
                )
            
            elif user_choice == "4":
                trans_id = input("Enter Transaction ID to remove: ").strip()
                confirmation = input(f"Are you sure you want to delete {trans_id}? (yes/no): ").strip()
                if confirmation.lower() == "yes":
                    transaction_manager.remove_transaction(trans_id)
            
            elif user_choice == "5":
                break
            
            else:
                print("Invalid option. Please try again.")
        
        except FinanceError as error:
            print(f"Error: {error}")

def manage_budgets(budget_manager):
    """Handles all budget-related operations"""
    while True:
        display_budget_menu()
        user_choice = input("Select an option: ").strip()
        
        try:
            if user_choice == "1":
                budget_manager.show_all_budgets()
            
            elif user_choice == "2":
                budget_id = input("Enter Budget ID: ").strip()
                budget_month = input("Enter Month (YYYY-MM): ").strip()
                budget_category = input("Enter Category: ").strip()
                budget_limit = input("Enter Limit Amount: ").strip()
                budget_manager.add_budget(budget_id, budget_month, budget_category, budget_limit)
            
            elif user_choice == "3":
                budget_id = input("Enter Budget ID to modify: ").strip()
                new_month = input("Enter new month (press Enter to skip): ").strip()
                new_category = input("Enter new category (press Enter to skip): ").strip()
                new_limit = input("Enter new limit amount (press Enter to skip): ").strip()
                budget_manager.modify_budget(
                    budget_id,
                    month=new_month if new_month else None,
                    category=new_category if new_category else None,
                    limit_amount=float(new_limit) if new_limit else None
                )
            
            elif user_choice == "4":
                budget_id = input("Enter Budget ID to remove: ").strip()
                confirmation = input(f"Are you sure you want to delete {budget_id}? (yes/no): ").strip()
                if confirmation.lower() == "yes":
                    budget_manager.remove_budget(budget_id)
            
            elif user_choice == "5":
                break
            
            else:
                print("Invalid option. Please try again.")
        
        except FinanceError as error:
            print(f"Error: {error}")

def main():
    """Main program function"""
    # Create manager objects
    account_manager = AccountManager()
    transaction_manager = TransactionManager()
    budget_manager = BudgetManager()
    
    print("\nWelcome to Personal Finance Manager!")
    
    # Try to load existing data when program starts
    try:
        account_manager.load_from_file()
        transaction_manager.load_from_file()
        budget_manager.load_from_file()
    except Exception as error:
        print(f"Note: Could not load previous data ({error}). Starting with empty data.")
    
    # Main program loop
    while True:
        display_main_menu()
        user_choice = input("Select an option: ").strip()
        
        try:
            if user_choice == "1":
                manage_accounts(account_manager)
            
            elif user_choice == "2":
                manage_transactions(transaction_manager)
            
            elif user_choice == "3":
                manage_budgets(budget_manager)
            
            elif user_choice == "4":
                account_manager.save_to_file()
                transaction_manager.save_to_file()
                budget_manager.save_to_file()
                print("All data has been saved successfully!")
            
            elif user_choice == "5":
                account_manager.load_from_file()
                transaction_manager.load_from_file()
                budget_manager.load_from_file()
                print("All data has been loaded successfully!")
            
            elif user_choice == "6":
                save_option = input("Do you want to save before exiting? (yes/no): ").strip()
                if save_option.lower() == "yes":
                    account_manager.save_to_file()
                    transaction_manager.save_to_file()
                    budget_manager.save_to_file()
                print("Thank you for using Personal Finance Manager. Goodbye!")
                break
            
            else:
                print("Invalid option. Please try again.")
        
        except FinanceError as error:
            print(f"Error: {error}")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break

if __name__ == "__main__":
    main()
