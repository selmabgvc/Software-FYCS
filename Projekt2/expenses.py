
class Expense:
    """Represents a single expense entry.

    Printing the object (print(expense)) uses `__str__` and will show:
        Expense: <name>, <category>, <amount> Dollar
    """

    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self) -> str:
        return f"Expense(name={self.name!r}, category={self.category!r}, amount={self.amount!r})"

    def __str__(self) -> str:
        # Format numeric amounts as German-style Euro: two decimals, comma as decimal
        # separator and the euro sign immediately after the number (e.g. 10,00€).
        if isinstance(self.amount, (int, float)):
            # Format with two decimals, then replace decimal point with comma.
            # Using formatting avoids floating point surprises for typical usage.
            amount_str = f"{self.amount:.2f}".replace('.', ',') + '€'
        else:
            amount_str = str(self.amount)
        return f"Expense: {self.name}, {self.category}, {amount_str}"

