# transaction_command.py

from abc import ABC, abstractmethod
from transaction.transaction_category import TransactionCategory


class ICommand(ABC):
    """Abstract base class for commands."""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class ApplyTransactionCommand(ICommand):
    """Command to apply a transaction to a balance."""

    def __init__(self, balance, transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        """Apply the transaction to the balance."""
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        if self.transaction.category == TransactionCategory.INCOME:
            self.balance.add_expense(self.transaction.amount)
        elif self.transaction.category == TransactionCategory.EXPENSE:
            self.balance.add_income(self.transaction.amount)


class TransactionInvoker:
    """Invoker that manages command history for undo/redo."""

    def __init__(self):
        self._history = []
        self._redo_stack = []

    def execute_command(self, command):
        command.execute()
        self._history.append(command)
        self._redo_stack = []

    def undo(self):
        if not self._history:
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        if not self._redo_stack:
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
