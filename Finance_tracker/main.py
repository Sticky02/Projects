import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amt, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "Finance_record.csv"
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_record(cls, date, amount, category, description):
        new_entry = {"date" : date,
                     "amount" : amount,
                     "category" : category,
                     "description" : description
                     }
        try:
            with open(cls.CSV_FILE, "a" , newline = "") as csvfile:
                fieldnames = ["date","amount","category","description"]
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                writer.writerow(new_entry)
            print("Entry added successfully")
        except Exception as e:
            print(f"Error adding entry: {e}")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
            start_date = datetime.strptime(start_date, cls.FORMAT)
            end_date = datetime.strptime(end_date, cls.FORMAT)
            
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]
            
            if filtered_df.empty:
                print("No transactions found.")
            else:
                print(f"Transaction from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
                print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))
                
                total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
                total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
                print("\nSummary: ")
                print(f"Total Income: Rs{total_income:.2f}")
                print(f"Total Expense: Rs{total_expense:.2f}")
                print(f"Net Savings: Rs{(total_income - total_expense):.2f}")
            return filtered_df
        except Exception as e:
            print(f"Error getting transactions: {e}")

def add():
    CSV.initialize_csv()
    date = input("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ")
    amount = float(input("Enter the amount: "))
    category = input("Enter the category (Income/Expense): ")
    description = input("Enter the description: ")
    CSV.add_record(date, amount, category, description)

def plot(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"]=="Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"]=="Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2.View transactions and summary within a date range")
        print("0.Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot(df)
        elif choice == "0":
            print("Exiting......")
            break
        else:
            print("Invalid choice. Enter 1,2 or 0.")

if __name__ == "__main__":
    main()