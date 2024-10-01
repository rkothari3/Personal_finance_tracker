# Import the necessary libraries to work with CSV files and manipulate dates and data
import pandas as pd  # Allows us to load and manipulate CSV files efficiently
import csv  # Provides tools to read from and write to CSV files
from datetime import datetime  # Used for handling date and time data
from Data_entry import get_amount, get_category, get_date, get_description  # Custom module to collect input data
import matplotlib.pyplot as plt  # Library for creating plots and visualizations

# Define a class to manage CSV-related operations
class CSV:
    # Class variables: shared across all instances of this class
    CSV_FILE = "finance_data.csv"  # Name of the CSV file where data will be stored
    COLUMNS = ["date", "amount", "category", "description"]  # Columns for the CSV file
    FORMAT = "%d-%m-%Y"  # Format for handling dates (day-month-year)

    # Initialize the CSV file if it doesn't exist
    @classmethod  # Class method: operates on the class, not instances of the class
    def intialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)  # Try loading the CSV file using pandas
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with the required columns
            df = pd.DataFrame(columns=cls.COLUMNS)  # Create an empty DataFrame with the specified columns
            df.to_csv(cls.CSV_FILE, index=False)  # Save the empty DataFrame as a CSV file

    # Add a new transaction entry to the CSV file
    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Create a dictionary to store the new transaction
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        # Open the CSV file in append mode to add a new entry
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)  # Create a CSV writer object
            writer.writerow(new_entry)  # Write the new entry as a row in the CSV file
        print("Entry added successfully!")  # Confirm the entry was added

    # Retrieve transactions within a specific date range
    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)  # Load the CSV file into a pandas DataFrame
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)  # Convert the 'date' column to datetime format

        # Convert input dates to datetime objects for comparison
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Create a mask to filter rows based on the date range
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]  # Select rows where the date is within the range

        # If no transactions match the date range, inform the user
        if filtered_df.empty:
            print('No transactions found in the given date range.')
        else:
            # Print the filtered transactions in a formatted manner
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(filtered_df.to_string(
                index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            # Calculate and display income, expenses, and net savings
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            return filtered_df  # Return the filtered DataFrame

# Function to add a transaction by interacting with the user
def add():
    CSV.intialize_csv()  # Ensure the CSV file is initialized
    # Get the transaction details from the user
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    # Add the entry to the CSV file
    CSV.add_entry(date, amount, category, description)

# Function to plot income and expenses over time
def plot_transactions(df):
    df.set_index('date', inplace=True)  # Set the date as the index for the DataFrame
    # Create DataFrames for income and expenses, resampled by day
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    
    # Plot the income and expenses on a line chart
    plt.figure(figsize=(10, 5))  # Set the size of the plot
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")  # Plot income in green
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")  # Plot expenses in red
    plt.xlabel("Date")  # Label the x-axis
    plt.ylabel("Amount")  # Label the y-axis
    plt.title('Income and Expenses Over Time')  # Set the title of the plot
    plt.legend()  # Add a legend to differentiate income and expenses
    plt.grid(True)  # Display a grid for better readability
    plt.show()  # Display the plot

# Main function that drives the program logic
def main():
    while True:  # Create an infinite loop to continuously show options to the user
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")  # Get the user's choice

        if choice == "1":  # If the user chooses to add a new transaction
            add()
        elif choice == "2":  # If the user chooses to view transactions
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            # Ask if the user wants to see a plot of income vs expenses
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":  # If the user chooses to exit
            print("Exiting...")
            break  # Exit the loop, thus ending the program
        else:  # If the user enters an invalid choice
            print("Invalid choice. Enter 1, 2, or 3.")

# Entry point for the program: only run the main function if the script is executed directly
if __name__ == "__main__":
    main()  # Run the main function
