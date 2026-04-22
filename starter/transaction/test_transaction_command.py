import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ApplyTransactionCommand, TransactionInvoker


class TestApplyTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_execute_income(self):
        t = Transaction(200, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(self.balance, t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), 200)

    def test_execute_expense(self):
        t = Transaction(50, TransactionCategory.EXPENSE)
        cmd = ApplyTransactionCommand(self.balance, t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), -50)

    def test_undo_income(self):
        t = Transaction(150, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(self.balance, t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), 150)
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_expense(self):
        t = Transaction(80, TransactionCategory.EXPENSE)
        cmd = ApplyTransactionCommand(self.balance, t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), -80)
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 0)


class TestTransactionInvoker(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.invoker = TransactionInvoker()

    def test_execute_and_undo(self):
        t = Transaction(100, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(self.balance, t)
        self.invoker.execute_command(cmd)
        self.assertEqual(self.balance.get_balance(), 100)
        self.invoker.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo(self):
        t = Transaction(100, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(self.balance, t)
        self.invoker.execute_command(cmd)
        self.invoker.undo()
        self.assertEqual(self.balance.get_balance(), 0)
        self.invoker.redo()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_multiple_undo_redo(self):
        t1 = Transaction(100, TransactionCategory.INCOME)
        t2 = Transaction(40, TransactionCategory.EXPENSE)
        cmd1 = ApplyTransactionCommand(self.balance, t1)
        cmd2 = ApplyTransactionCommand(self.balance, t2)

        self.invoker.execute_command(cmd1)
        self.invoker.execute_command(cmd2)
        self.assertEqual(self.balance.get_balance(), 60)

        self.invoker.undo()
        self.assertEqual(self.balance.get_balance(), 100)

        self.invoker.undo()
        self.assertEqual(self.balance.get_balance(), 0)

        self.invoker.redo()
        self.assertEqual(self.balance.get_balance(), 100)

        self.invoker.redo()
        self.assertEqual(self.balance.get_balance(), 60)

    def test_undo_with_no_history(self):
        self.invoker.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo_with_no_history(self):
        self.invoker.redo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_new_command_clears_redo_stack(self):
        t1 = Transaction(100, TransactionCategory.INCOME)
        t2 = Transaction(50, TransactionCategory.EXPENSE)
        cmd1 = ApplyTransactionCommand(self.balance, t1)
        cmd2 = ApplyTransactionCommand(self.balance, t2)

        self.invoker.execute_command(cmd1)
        self.invoker.undo()
        self.invoker.execute_command(cmd2)
        self.invoker.redo()
        self.assertEqual(self.balance.get_balance(), -50)


if __name__ == "__main__":
    unittest.main()
