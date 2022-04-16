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
    """
    print("Please enter goals data from the last season.")
    print("Data should be eight numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60,25,30\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")


get_goals_data()