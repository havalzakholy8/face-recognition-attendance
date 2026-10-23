# exceptions.py
# Custom exception classes for the finance app

class FinanceError(Exception):
    """Main exception class for finance app errors"""
    pass

class ValidationError(FinanceError):
    """Exception for when user input is invalid"""
    pass

class NotFoundError(FinanceError):
    """Exception for when we can't find something"""
    pass

class StorageError(FinanceError):
    """Exception for when saving/loading files fails"""
    pass
