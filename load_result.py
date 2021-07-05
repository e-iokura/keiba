from config import app_setting
from sys import argv
from modules import race_module
from modules import date_module

RACE_ID = "202005021211"

#Load the date of this month and register it in the DB
def load_kaisai_dates():
    date_module.load_dates()

def insert_race_result():
    race_result_data = race_module.insert_race_result(RACE_ID)

if __name__ == '__main__':
    app_setting.set_const_values()

    kaisi_dates = load_kaisai_dates(argv[0], argv[1])

    print("終了")
