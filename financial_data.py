from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, default=False):
    user_date = input(prompt)

    if default and not user_date:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.today().strptime(user_date, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date. Please provide your date in dd-mm-yyyy format.")
        return get_date(prompt, default)


def get_amount():
    try:
        user_amount = float(input("Enter your amount: "))

        if user_amount <= 0:
            raise ValueError("The amount must be non-zero and positive.")
        return user_amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    user_category = input("Enter the category ('I' for Income or 'E' for Expense): ").strip().upper()

    if user_category in CATEGORIES:
        return CATEGORIES[user_category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_desc():
    return input("Enter the description (Optional): ").capitalize()
