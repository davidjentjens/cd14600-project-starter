# balance.py

from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""

    _instance = None
    _balance = 0

    @classmethod
    def get_instance(cls):
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        if Balance._instance is not None:
            raise Exception("Balance is a singleton")
        Balance._instance = self
        Balance._balance = 0

    def reset(self):
        """Reset the net balance to zero."""
        Balance._balance = 0

    def add_income(self, amount):
        """Add income to the balance."""
        Balance._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        Balance._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError("Invalid transaction category")

    def get_balance(self):
        """Get the current net balance."""
        return Balance._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: ${Balance._balance:.2f}"
    
