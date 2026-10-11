# 🐍 Python Personal Expense Tracker

A simple and interactive command-line Personal Expense Tracker application built with Python. It allows users to manage their daily expenses, track categories, check budgets, view expenses grouped by category, search through descriptions/categories, and visualize expenses using a dynamic Turtle graphics bar chart.

---

## 🚀 Features

- **Add Expenses:** Input and validate dates (`YYYY-MM-DD`), numeric amounts, categories, and descriptions. Data is automatically saved to file.
- **View Expenses:** Display all recorded expenses or view them grouped neatly by category.
- **Visual Bar Chart:** Generates an interactive Turtle graphics bar chart with auto-scaled dimensions, centered multiline text, and categorized totals.
- **Keyword Search:** Filter and search expenses instantly by keywords (case-insensitive).
- **Budget Alerts:** Compares your category spending against predefined budget limits from a budget file and triggers alerts if you exceed them.
- **Robust Error Handling:** Validates user inputs (dates and numerical amounts) to prevent crashes and handles missing files gracefully.

---

## 📁 Project Structure

```text
├── Personal_Expense_Tracker.py   # Main Python source code
├── expenses.txt                  # Data storage file for expenses
└── budget.txt                    # Data storage file for category budgets
