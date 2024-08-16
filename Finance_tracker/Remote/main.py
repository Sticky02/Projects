import pandas as pd
from datetime import datetime
from data_entry import get_date
import matplotlib.pyplot as plt
from database import DBrun, Function

FORMAT = "%d-%m-%Y"

def Disp(start_date, end_date):
    try:
        col = Function.col
        df = col.find({},{"_id":0})
        df = pd.DataFrame(df)
        df["date"] = pd.to_datetime(df["date"], format = FORMAT)
        start_date = datetime.strptime(start_date, FORMAT)
        end_date = datetime.strptime(end_date, FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
            
        if filtered_df.empty:
            print("No transactions found.")
        else:
            print(f"Transaction from {start_date.strftime(FORMAT)} to {end_date.strftime(FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(FORMAT)}))
            total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: Rs{total_income:.2f}")
            print(f"Total Expense: Rs{total_expense:.2f}")
            print(f"Net Savings: Rs{(total_income - total_expense):.2f}")
            return filtered_df
    except Exception as e:
            print(f"Error getting transactions: {e}")

def plot(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"] == "Income"].reindex(df.index, fill_value = 0)
    expense_df = df[df["category"] == "Expense"].reindex(df.index, fill_value = 0)
    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():#driver

    DB = Function()
    print("Welcome to Finance Tracker.")
    print("Please select an option from the menu below:")

    while True:
        print("1. Manage Records")
        print("2. View Records")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            DBrun()
        
        elif choice == "2":
            loop = True
            while loop:
                print("1. View all records.")
                print("2. View records by date range.")
                print("0. Back")
                ch = input("Enter your choice: ")
                if ch == "1":
                    DB.display()
                    df = DB.col.find({},{"_id":0})
                    df = pd.DataFrame(df)
                    if input("Do you want to see a plot? (y/n) ").lower() == "y":
                        plot(df)
                elif ch == "2":
                    start_date = input("Enter start date: ")
                    end_date = input("Enter end date: ")
                    df = Disp(start_date, end_date)
                    if input("Do you want to see a plot? (y/n) ").lower() == "y":
                        plot(df)
                elif ch == "0":
                    loop = False
                else:
                    print("Invalid choice. Please try again.")
            
        elif choice == "0":
            print("Exiting....")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
