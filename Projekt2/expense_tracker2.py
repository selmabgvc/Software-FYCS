from expense import Expense
import calendar
import datetime
import os



#   HEADERS & FARBE

def print_header(title: str):
    line = "=" * 40
    print(f"\n{line}")
    print(title.center(40))
    print(f"{line}\n")


def print_subheader(title: str):
    line = "-" * 40
    print(f"\n{line}")
    print(title.center(40))
    print(f"{line}\n")


def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def print_progress_bar(spent: float, budget: float):
    """Zeigt einen einfachen Fortschrittsbalken basierend auf dem Budget."""
    if budget <= 0:
        print("No valid budget set.")
        return

    ratio = max(0.0, min(spent / budget, 1.0))  # auf [0,1] begrenzen
    bar_length = 30
    filled_length = int(bar_length * ratio)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    percent = ratio * 100

    # Farbe je nach Auslastung
    if ratio < 0.75:
        line = green(f"[{bar}] {percent:5.1f}% of budget used")
    elif ratio < 1.0:
        line = yellow(f"[{bar}] {percent:5.1f}% of budget used")
    else:
        line = red(f"[{bar}] {percent:5.1f}% of budget used (over budget)")
    print(line)


#                 MAIN


def main():
    expense_file_path = "expenses.csv"
    budget = 2000.0

    print_header("EXPENSE TRACKER")

    while True:
        print_subheader("MAIN MENU")
        print("1) Add new expense")
        print("2) Show monthly summary")
        print("3) Exit\n")

        choice = input("Select an option [1-3]: ").strip()

        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == "2":
            summarize_expenses(expense_file_path, budget)
        elif choice == "3":
            print("\nExiting. Goodbye.\n")
            break
        else:
            print("\nInvalid option. Please select 1, 2 or 3.\n")



#        USER INPUT & SPEICHERN

def get_user_expense() -> Expense:
    print_subheader("NEW EXPENSE ENTRY")

    print("Please tell me what you've spent money on.\n")
    expense_name = input("Enter name: ").strip()
    expense_amount = float(input("Enter amount: "))

    expense_categories = [
        "Food",
        "Home",
        "Car",
        "Fun",
        "Misc",
    ]

    while True:
        print("\nPlease select one of the following categories:")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount,
            )
            return new_expense
        else:
            print("\nThat is an invalid category. You might want to try again!")


def save_expense_to_file(expense: Expense, expense_file_path: str):
    print_subheader("SAVED")
    print(f"{expense}\n")

    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")



#              AUSWERTUNG


def summarize_expenses(expense_file_path: str, budget: float):
    # Falls es noch keine Datei gibt
    if not os.path.exists(expense_file_path):
        print_subheader("EXPENSE SUMMARY")
        print("No expenses recorded yet.\n")
        return

    now = datetime.datetime.now()
    month_name = now.strftime("%B").upper()
    year = now.year

    print_header(f"{month_name} {year} - SUMMARY")

    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    if not expenses:
        print("No expenses recorded yet.\n")
        return

    # Summen nach Kategorie
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Your Expenses By Category:")
    for key, amount in amount_by_category.items():
        print(f"  {key:<10}: {amount:8.2f}€")
    print()

    total_spent = sum(x.amount for x in expenses)
    remaining_budget = budget - total_spent
    remaining_ratio = remaining_budget / budget if budget > 0 else 0.0

    print_progress_bar(total_spent, budget)
    print()

    print(f"You've spent a total of:     {total_spent:8.2f}€")
    print(f"Remaining monthly budget:   {remaining_budget:8.2f}€")

    # Warnung bei unter 15 % Restbudget
    if remaining_budget < 0:
        print(red("\nYou have exceeded your budget. Further spending should be reduced.\n"))
    elif remaining_ratio < 0.15:
        print(yellow("\nWarning: Less than 15% of your budget remains. Consider reducing expenses.\n"))

    # Budget pro Tag
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(
            green(
                f"If you want to stay within your budget, "
                f"you can spend approximately {daily_budget:.2f}€ per remaining day.\n"
            )
        )
    else:
        print("This is the last day of the month. No daily budget calculation.\n")


#              ENTRYPOINT

if __name__ == "__main__":
    main()
