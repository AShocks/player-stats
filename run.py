import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

        data_str = input("Enter your data here: ")

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


def update_goals_worksheet(data):
    """
    Update goals worksheet, add new row with the list data provided
    """
    print("Updating goals worksheet...\n")
    goals_worksheet = SHEET.worksheet("goals")
    goals_worksheet.append_row(data)
    print("Goals worksheet updated successfully.\n")


def goal_involvement(goals_row):
    """
    Goals plus assists gives the overall involvement in goals scored per player
    """
    print("Calculating goal_involvement data...\n")
    assists = SHEET.worksheet("assists").get_all_values()
    assists_row = assists[-1]
    print(assists_row)



def main():
    """
    Run all program functions
    """
    data = get_goals_data()
    goals_data = [int(num) for num in data]
    update_goals_worksheet(goals_data)
    goal_involvement(goals_data)



print("Welcome to PlayerStats Data Automation")
main()