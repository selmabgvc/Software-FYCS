# Projekt 2 von Selma Begovic und Yvonne Kaderavek

# Expense Tracker

A simple command-line **Expense Tracker** written in Python.  
You can add expenses, categorize them, and see a monthly summary including budget usage and a daily spending recommendation.

---

## Features

  - Add new expenses with:
    - name
    - amount
    - category (e.g. `Food`, `Home`, `Car`, `Fun`, `Misc`)
  - Store expenses in a CSV file (`expenses.csv`) next to the script
  - Show a **monthly summary**, including:
    - Total spent
    - Expenses grouped by category
    - Remaining budget
  - Simple **progress bar** for budget usage
  - Daily spending recommendation based on remaining days in the month
  - Warnings when:
    - budget is exceeded
    - less than 15% of budget remains
  - Colored terminal output for better readability (green / yellow / red)
