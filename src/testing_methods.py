from datetime import datetime

# Copyright Vincent Salter 02/12/23 2nd of May 2024

class UpdateData:
    @staticmethod
    def update_drawdown_percent(stock_algo, new_value):
        try:
            new_value = float(new_value)
            if new_value <= 0:
                print("Drawdown percent must be greater than 0.")
            else:
                stock_algo.set_drawdown_percent(new_value)
                print(f"Drawdown percent updated to {new_value}%.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    @staticmethod
    def update_day_range(stock_algo, new_value):
        try:
            new_value = int(new_value)
            if new_value <= 0:
                print("Day range must be a positive integer.")
            else:
                stock_algo.set_day_range(new_value)
                print(f"Day range updated to {new_value} days.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def update_date_range(stock_algo, start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date > end_date:
                print("Start date cannot be after end date.")
            else:
                stock_algo.set_date_range(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                print(f"Date range updated from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")

    
    def update_all(stock_algo):
        UpdateData.update_drawdown_percent(stock_algo)
        UpdateData.update_day_range(stock_algo)
        UpdateData.update_date_range(stock_algo)


def update_stock_algo(stock_algo):
    print("\n***Reminder: Type 'back' at any point to return to the main menu or 'exit' to end updating.***")
    while True:
        print("\n1. Update Drawdown Percent\n2. Update Day Range\n3. Update Date Range\n4. Update All\n5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            new_value = input("Enter new drawdown percent or 'back' to return: ").strip()
            if new_value.lower() != 'back':
                UpdateData.update_drawdown_percent(stock_algo, new_value)
        elif choice == '2':
            new_value = input("Enter new day range or 'back' to return: ").strip()
            if new_value.lower() != 'back':
                UpdateData.update_day_range(stock_algo, new_value)
        elif choice == '3':
            new_value = input("Enter new start date, new end date (comma seperated, YYYY-MM-DD) or 'back' to return: ").strip()
            if new_value.lower() != 'back':
                start_date, end_date = new_value.split(',')
                UpdateData.update_date_range(stock_algo, start_date.strip(), end_date.strip())
        elif choice == '4':
            new_value = input("Proceed to update all settings or 'back' to return: ").strip()
            if new_value.lower() != 'back':
                UpdateData.update_all(stock_algo)
        elif choice == '5' or choice.lower() == 'exit':
            print("Exiting to main program...")
            break
        else:
            print("Invalid choice. Please try again.")
