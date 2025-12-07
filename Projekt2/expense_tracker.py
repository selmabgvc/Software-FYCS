try:
    # When started as a package (python -m Projekt2.expense_tracker)
    from .expenses import Expense
except Exception:
    # Fallback: when running the file directly (python Projekt2/expense_tracker.py)
    from expenses import Expense
    from pathlib import Path

from pathlib import Path


def main():
    print(f"Running Expense Tracker!")
    # Store the CSV next to this module so it lives inside the Projekt2 folder
    expenses_file_path = Path(__file__).resolve().parent / "expenses.csv"
    expenses_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Get user to input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expenses_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expenses_file_path)


def get_user_expense(): 
    print(f"Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food", 
        "🏠 Home", 
        "🎉 Entertainment", 
        "🚙 Car", 
        "❓ Other"
    ]

    while True: 
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"   {i +1}. {category_name}")

        values_range = f"[1 - {len(expense_categories)}]"
        # try error handling for non integer inputs - look it up
        selected_index = int(input(f"Enter a category number {values_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again.")



def save_expense_to_file(expense: Expense, expenses_file_path):
    print(f"Saving User Expense: {expense} to {expenses_file_path}")
    with open(expenses_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")

def summarize_expenses(expenses_file_path):
    print(f"Summarizing User Expenses")
    try:
        with open(expenses_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                print(f"Total expenses recorded: {len(lines)}")
                for line in lines:
                    print(f"  {line.strip()}")
            else:
                print("No expenses recorded yet.")
    except FileNotFoundError:
        print(f"No expenses file found: {expenses_file_path}")

if __name__ == "__main__":
    main()
