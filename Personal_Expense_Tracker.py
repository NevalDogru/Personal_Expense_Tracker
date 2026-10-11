import turtle
from datetime import datetime
import os


def read_file(file_name):
	# Reads a file.
	try:
		with open(file_name, 'r') as file:
			return [line.strip() for line in file if line.strip()]  # Skip empty lines
	except FileNotFoundError:
		print(f"Warning: {file_name} not found.")
		return []


def write_file(file_name, data):
	# Writes a list of strings to a file.
	with open(file_name, 'w') as file:
		for line in data:
			file.write(line + '\n')


def separate_expenses(lines):
	# Separate lines into a list of expenses.
	expenses = []
	for line in lines:
		data = line.split('\t')
		if len(data) >= 4:
			# Join descriptions if they contain accidental tabs
			date, amount, category = data[0], data[1], data[2]
			description = " ".join(data[3:])
			expenses.append([date, amount, category, description])
	return expenses


def separate_budget(lines):
	# Separate lines into a budget dictionary.
	budget = {}
	for line in lines:
		data = line.split('\t')
		if len(data) == 2:
			try:
				# Standardize budget categories with capitalize
				budget[data[0].strip().capitalize()] = float(data[1])
			except ValueError:
				continue  # Skip faulty lines
	return budget


def add_expense(expenses, file_name):
	# Adds a new expense and writes it to the file.

	# Loop until a valid date format is entered
	while True:
		date = input("Please enter date (YYYY-MM-DD): ")
		try:
			datetime.strptime(date, "%Y-%m-%d")
			break  # Break loop if a valid format is entered
		except ValueError:
			print("Invalid date format or value. Please enter a valid date in YYYY-MM-DD format.")

	# Loop until a valid amount is entered
	while True:
		try:
			amount = float(input("Please enter amount: "))
			break
		except ValueError:
			print("Invalid input. Please enter a numerical value for the amount.")

	category = input("Please enter category: ").strip().capitalize()  # Standardize category
	description = input("Please enter description: ")

	new_expense = [date, str(amount), category, description]
	expenses.append(new_expense)

	# Update file on each addition
	write_file(file_name, ["\t".join(expense) for expense in expenses])
	print("Your expense has been successfully added to the file.")


def view_expenses(expenses):
	# See all expenses.
	print("\nAll Expenses:")
	if not expenses:
		print("No expenses recorded yet.")
		return
	for expense in expenses:
		print("\t".join(expense))


def view_expenses_grouped(expenses):
	# Group expenses by category
	grouped = {}

	for expense in expenses:
		category = expense[2].capitalize()  # Standardize category casing
		if category not in grouped:
			grouped[category] = []
		grouped[category].append(expense)

	print("\nExpenses by Category:")
	if not grouped:
		print("No expenses recorded yet.")
		return

	for category, items in grouped.items():
		print(f"\n{category}:")
		for item in items:
			print("\t".join(item))


def draw_bar_chart(expenses):
	# Draws a bar chart of expenses
	if not expenses:
		print("\nNo data to draw a chart.")
		return

	categories = {}
	for expense in expenses:
		category = expense[2].capitalize()  # Standardize category casing
		try:
			amount = float(expense[1])
			categories[category] = categories.get(category, 0) + amount
		except ValueError:
			continue

	if not categories:
		return

	wn = turtle.Screen()
	wn.title("Expense Bar Chart")
	wn.bgcolor("#89CFF0")

	max_height = max(categories.values())
	num_bars = len(categories)

	# Adjusted variables for perfectly centered multiline text
	border = 60
	gap = 70
	bar_width = 40

	# Scale screen width properly
	total_width = (bar_width + gap) * num_bars
	# Y ekseni penceresini yazilarin sigmasi icin biraz daha yukselt
	wn.setworldcoordinates(0 - border, 0 - border, total_width + border, max_height + border * 1.5)

	alex = turtle.Turtle()
	alex.speed(0)
	alex.color("black")
	alex.fillcolor("deeppink")
	alex.pensize(4)

	for i, (category, total) in enumerate(categories.items()):
		alex.begin_fill()

		# Sol kenar (Yukari)
		alex.left(90)
		alex.forward(total)

		# Ust kenarin yarisina kadar git (Tam ortaya hizalanmak icin)
		alex.right(90)
		alex.forward(bar_width / 2)

		# Yaziyi cubugun sinirina degmemesi icin 10 piksel yukariya yazdir
		alex.penup()
		alex.left(90)
		alex.forward(10)
		# Kategori ve tutari \n ile iki satira bolup merkeze ortala
		alex.write(f"{category}\n{total:.2f}", align="center", font=("Arial", 9, "bold"))
		alex.backward(10)
		alex.right(90)
		alex.pendown()

		# Ust kenarin kalan yarisini ciz
		alex.forward(bar_width / 2)

		# Sag kenar (Asagi)
		alex.right(90)
		alex.forward(total)

		alex.left(90)
		alex.end_fill()

		# Diger cubuga gecis boslugu
		alex.penup()
		alex.forward(gap)
		alex.pendown()

	alex.hideturtle()
	wn.exitonclick()


def search_keyword(expenses):
	# Searches for expenses by keyword
	keyword = input("Please enter keyword to search: ").lower()
	result = False

	print("\nSearch Results:")
	for expense in expenses:
		# Search only in category or description, case-insensitive
		if keyword in expense[2].lower() or keyword in expense[3].lower():
			print("\t".join(expense))
			result = True

	if not result:
		print(f"The keyword you entered could not be found: {keyword}. You are directed to the menu.")


def check_budget_alert(expenses, budget):
	# Checks if expenses exceed the budget in any category.
	categories = {}
	for expense in expenses:
		category = expense[2].capitalize()  # Standardize category casing
		try:
			amount = float(expense[1])
			categories[category] = categories.get(category, 0) + amount
		except ValueError:
			continue

	print("\nBudget Alerts:")
	exceeded = False

	# Check budget alerts
	for category, total in categories.items():
		if category in budget and total > budget[category]:
			exceeded = True
			print(f"Alert: Over budget in {category}. Spent: {total:.2f}, Budget: {budget[category]:.2f}")

	if not exceeded:
		print("You have no expenses exceeding the budget.")


def main():
	# Automatically find the absolute path of the directory containing this script
	base_dir = os.path.dirname(os.path.abspath(__file__))

	# Construct absolute paths for the data files
	expenses_file = os.path.join(base_dir, "expenses.txt")
	budget_file = os.path.join(base_dir, "budget.txt")

	expenses_data = read_file(expenses_file)
	budget_data = read_file(budget_file)

	expenses = separate_expenses(expenses_data)
	budget = separate_budget(budget_data)

	while True:
		print("\nMenu:")
		print("1. Add Expense")
		print("2. View Expenses")
		print("3. Produce Bar Chart for Expenses")
		print("4. Search/Filter")
		print("5. Budget Alerts")
		print("6. Exit")

		choice = input("Please select a number to continue (1-6): ").strip()

		if choice == "1":
			add_expense(expenses, expenses_file)
		elif choice == "2":
			print("\n1. View All Expenses")
			print("2. View Expenses by Category")
			next_choice = input("Please select a number to continue (1-2): ").strip()

			if next_choice == "1":
				view_expenses(expenses)
			elif next_choice == "2":
				view_expenses_grouped(expenses)
			else:
				print("Your selection did not match. Please try again.")
		elif choice == "3":
			draw_bar_chart(expenses)
		elif choice == "4":
			search_keyword(expenses)
		elif choice == "5":
			check_budget_alert(expenses, budget)
		elif choice == "6":
			# Save the list one last time before exiting
			write_file(expenses_file, ["\t".join(expense) for expense in expenses])
			print("Logged out successfully. Have a great day!")
			break
		else:
			print("Your selection did not match. Please try again. You are directed to the menu.")


if __name__ == "__main__":
	main()