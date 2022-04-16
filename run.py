import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('player_stats')


def get_goals_data():
    """
    Get goals figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 8 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """

    while True:
        print("Please enter goals data from the last season.")
        print("Data should be eight numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60,20,10\n")

        data_str = input("Enter your data here:\n")

        goals_data = data_str.split(",")

        if validate_data(goals_data):
            print("Data is valid!")
            break

    return goals_data



def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into integers,
    or if there aren't exactly 8 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 8:
            raise ValueError(
                f"Exactly 8 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True





def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def goal_involvement(goals_row):
    """
    Goals plus assists gives the overall involvement in goals scored per player
    """
    print("Calculating goal_involvement data...\n")
    assists = SHEET.worksheet("assists").get_all_values()
    assists_row = assists[-1]
    goal_involvement_data = []
    for goals, assists in zip(goals_row, assists_row):
        involvement = int(goals) + assists
        goal_involvement_data.append(involvement)
    
    return goal_involvement_data

def get_last_5_entries_goals():
    """
    Collects columns of data from goals worksheet, collecting
    the last 5 entries for each player and returns the data
    as a list of lists.
    """
    goals = SHEET.worksheet("goals")

    columns = []
    for ind in range(1, 9):
        column = goals.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_goals_data(data):
    """
    Calculate the average goals scored for each player
    """
    print("Calculating goals data...\n")
    new_goals_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average
        new_goals_data.append(round(stock_num))

    return new_goals_data



def main():
    """
    Run all program functions
    """
    data = get_goals_data()
    goals_data = [int(num) for num in data]
    update_worksheet(goals_data, "goals")
    goals_columns = get_last_5_entries_goals()
    assists_data = calculate_goals_data(goals_columns)
    update_worksheet(assists_data, "assists")
    print(assists_data)



print("Welcome to PlayerStats Data Automation")
main()

