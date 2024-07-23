import pandas as pd
import csv
from financial_data import get_date, get_category, get_amount, get_desc
from datetime import datetime
import matplotlib.pyplot as plt


class CSV:

    CSV_FILE = "my_finance_data.csv"
    ROW_NAMES = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.ROW_NAMES)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline='') as data_file:
            writer = csv.DictWriter(data_file, fieldnames=cls.ROW_NAMES)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transaction_history(cls, start_date, end_date):
        df = pd.read_csv(CSV.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_data = df.loc[mask]

        if filtered_data.empty:
            print("No transactions found in given date range.")
        else:
            print(f"Transaction history from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_data.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_data[filtered_data["category"] == "Income"]["amount"].sum()
            total_expense = filtered_data[filtered_data["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Net Savings: {(total_income - total_expense):.2f}")
        return filtered_data


def add_data():
    date = get_date("Enter the date (dd-mm-yyyy): ", default=True)
    amount = get_amount()
    category = get_category()
    description = get_desc()

    CSV.initialize()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Chart")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    print("\n1. Add new transaction.")
    print("\n2. View transaction summary.")
    print("\n3. Exit")
    
    while True:
        user_choice = int(input("Enter your choice (1-3): "))
        
        if user_choice == 1:
            add_data()
        elif user_choice == 2:
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transaction_history(start_date, end_date)
            if input("Do you want to see transaction chart?(y/n): ").lower() == "y":
                plot_transactions(df)
        elif user_choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")
            

if __name__ == "__main__":
    main()
