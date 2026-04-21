# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"Balance updated: {balance.get_balance()}")
        print(f"Transaction: {transaction}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance.get_balance() < self.threshold:
            print(f"Low balance alert: {balance.get_balance()}")
            print(f"Transaction: {transaction}")
