# Copyright Vincent Salter 02/12/23 2nd of May 2024

class UpdateData():

    def update_drawdown_percent(stock_algo):
        try:
            new_drawdown_percent = float(input("Input new drawdown percentage: "))
            stock_algo.set_drawdown_percent(new_drawdown_percent)
            print("\nDrawdown percentage updated successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def update_day_range(stock_algo):
        try:
            new_day_range = int(input("Input new day range: "))
            stock_algo.set_day_range(new_day_range)
            print("\nDay range updated successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    def update_date_range(stock_algo):
        new_start_date = input("Enter new start date: ")
        new_end_date = input("Enter new end date: ")
        stock_algo.set_date_range(new_start_date, new_end_date)
        print("\nDate range updated successfully.")

    def update_all(stock_algo):
        UpdateData.update_drawdown_percent(stock_algo)
        UpdateData.update_day_range(stock_algo)
        UpdateData.update_date_range(stock_algo)

    def update_stock_algo(stock_algo):
        print("\n***Reminder: Option 5 must be pressed to return to the main program.***")
        while True:
            print("\n1. Update Drawdown Percent\n2. Update Day Range\n3. Update Date Range\n4. Update All\n5. Exit")
            choice = input("Choose an option (1-5): ").strip()

            if choice == '1':
                UpdateData.update_drawdown_percent(stock_algo)
            elif choice == '2':
                UpdateData.update_day_range(stock_algo)
            elif choice == '3':
                UpdateData.update_date_range(stock_algo)
            elif choice == '4':
                UpdateData.update_all(stock_algo)
            elif choice == '5' or choice.lower() == 'exit':
                print("Exiting to main program...")
                break
            else:
                print("Invalid choice. Please try again.")
