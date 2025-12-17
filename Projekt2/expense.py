class Expense:
    """Represents a single expense entry.

    Printing the object (print(expense)) uses `__str__` and will show:
        Expense: <name>, <category>, <amount> Euro
    """

    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self) -> str:
        return f"Expense(name={self.name}, category={self.category}, amount={self.amount:.2f}€)"
     