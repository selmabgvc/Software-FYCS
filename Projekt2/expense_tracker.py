from expense import Expense
import calendar
import datetime


def main():
    print(f"\nLet's track your spending!\n")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print(f"Please tell me what you've spent money on.\n")
    expense_name = input("Enter name: ")
    expense_amount = float(input("Enter amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "🚗 car",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("\nPlease select one of the following categoies: \n")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print(red("\nThat is an invalid category. You might want to try again!\n"))


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"\nSo, let's save your expenses {expense} to {expense_file_path}\n")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print(f"\nLet's take a look at your expenses so far.\n")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("\nYour Expenses By Category:\n")
    for key, amount in amount_by_category.items():
        print(f"  {key}: {amount:.2f}€")

    total_spent = sum([x.amount for x in expenses])
    print(f"\nYou've spent a total of {total_spent:.2f}€\n")
    if total_spent > budget:
        # New user-friendly warning message when over budget
        print(red("\nOh, dear! It looks like we've past the your set limit for the budget. "
                  "You will have to be careful with any further spending.\n"))

    remaining_budget = budget - total_spent
    print(f"\nWhich means you still have {remaining_budget:.2f}€ left in your budget.\n")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"If you want to be within your budget. You will have {daily_budget:.2f}€ to spend on a daily basis."))


def green(text):
    return f"\033[92m{text}\033[0m"
def red(text):
    return f"\033[91m{text}\033[0m"


if __name__ == "__main__":
    main()
