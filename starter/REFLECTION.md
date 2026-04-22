# Design Pattern Reflection

## Singleton — Balance

The Balance class uses the Singleton pattern because there should only ever be one source of truth for the user's balance. If multiple Balance objects existed, they could drift out of sync and produce incorrect totals. The `get_instance()` classmethod ensures every part of the app references the same object, and the guarded `__init__` prevents accidental direct instantiation.

One trade-off is testability — since state persists across tests, each test must call `reset()` in `setUp` to avoid leaking state. In a larger app, dependency injection might be preferable, but for this scope the Singleton keeps things simple.

## Adapter — TransactionAdapter

The app's internal model uses `Transaction` objects with an `amount` and a `TransactionCategory`. External data sources (like the freelance platform) use a completely different structure with fields like `invoice_id`, `description`, and `typ`. The Adapter bridges this gap without modifying either side.

`TransactionAdapter` wraps an `ExternalFreelanceIncome` and exposes a `to_transaction()` method that maps the external fields to internal ones. This keeps the core Transaction class clean and makes it straightforward to add adapters for other external sources in the future.

## Observer — Balance Observers

The Observer pattern decouples the Balance from the things that react to its changes. `Balance` doesn't need to know whether it's printing updates, triggering alerts, or doing both — it just notifies its observers after each transaction.

I implemented two observers: `PrintObserver` logs every balance change, and `LowBalanceAlertObserver` tracks whether the balance has dropped below a configurable threshold. The `alert_triggered` flag resets when the balance recovers, so it reflects the current state rather than a one-time event.

The main challenge was deciding where to initialize the `_observers` list in a Singleton. Putting it as a class variable (rather than in `__init__`) ensures it survives across `reset()` calls, which only clear the balance — not the registered observers.

## Command — Undo/Redo Transactions

I chose the Command pattern because undo/redo is a natural fit for a finance app. Each `ApplyTransactionCommand` wraps a transaction and knows how to both execute and reverse it. The `TransactionInvoker` maintains a history stack and a redo stack, so undoing and redoing is just popping and pushing between them.

The undo logic reverses each transaction by calling the opposite method — undoing income calls `add_expense`, and vice versa. One thing to be aware of is that undo bypasses `apply_transaction`, so observers aren't notified on undo. For this project that's acceptable, but in production you'd want to decide whether reversals should trigger alerts too.
