# Personal Finance Manager

A command-line Python application for managing personal finances: accounts, income and expense transactions, and monthly budgets, with all data saved to CSV files.

*Built for the Python course in my master's program, 2025.*

## Features

- **Accounts** — create, view, modify and delete cash or bank accounts in different currencies (HUF, EUR, USD)
- **Transactions** — record income and expenses; expenses are automatically stored as negative amounts and income as positive
- **Budgets** — set monthly spending limits per category
- **CSV storage** — data loads automatically at startup and can be saved or reloaded from the menu
- **Input validation** — custom exceptions (`ValidationError`, `NotFoundError`, `StorageError`) catch invalid input and missing records
- **Tested** — 17 unit, integration and system tests with pytest

## Tech

- Python 3 (standard library only: `csv`, `os`)
- Object-oriented design with inheritance (`CashAccount` / `BankAccount`, `ExpenseTransaction` / `IncomeTransaction`)
- pytest for testing

## Project structure

```
personal_finance/
├── main.py                  # Menu-driven entry point
├── exceptions.py            # Custom exception classes
├── models/                  # Account, Transaction and Budget classes
├── managers/                # Create, read, update, delete logic for each model
├── storage/
│   └── csv_storage.py       # Reading and writing CSV files
├── tests/
│   └── test_finance.py      # Unit, integration and system tests
├── accounts.csv             # Sample data
├── transactions.csv         # Sample data
└── budgets.csv              # Sample data
```

## Getting started

```bash
git clone https://github.com/USERNAME/personal-finance-manager.git
cd personal-finance-manager
python main.py
```

No external packages are needed to run the app. The repo includes sample accounts, transactions and budgets so you can try it right away.

### Example: recording an expense

1. Choose `2` (Manage Transactions), then `2` (Add New Transaction)
2. Enter an ID (`T5`), account ID (`A1`), date (`2024-11-17`), amount (`5000`), description, category (`food`) and type (`expense`)
3. Choose `5` to return, then `4` to save everything to CSV

## Running the tests

```bash
pip install -r requirements.txt
pytest tests/test_finance.py -v
```

## Author

Haval Mustafa — [LinkedIn](https://www.linkedin.com/in/haval-mustafa-0834763a5/)
