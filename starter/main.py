"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_command import TransactionInvoker, ApplyTransactionCommand


def main():
    print("Adding transactions...")
   
    # TODO: Create balance and add observers
    balance = Balance.get_instance()
    balance.register_observer(LowBalanceAlertObserver(100))
    balance.register_observer(PrintObserver())

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # TODO: Apply all transactions to balance
    invoker = TransactionInvoker()
    for transaction in all_transactions:
        command = ApplyTransactionCommand(balance, transaction)
        invoker.execute_command(command)

    print("Transactions applied. Undoing last transaction...")
    invoker.undo()
    print("Redoing last transaction...")
    invoker.redo()

    print("Transactions applied. Undoing last transaction...")
    invoker.undo()
    print("Redoing last transaction...")
    invoker.redo()

if __name__ == "__main__":
    main()
