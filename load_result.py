from config import app_setting
from sys import argv
import datetime
from modules import date_module
from modules import race_result_module

if __name__ == '__main__':
    app_setting.set_const_values()

    today = datetime.date.today()
    year = today.year
    month = today.month
    if len(argv) >= 3:
        year = argv[1]
        month = argv[2]
    #Load the date of this month and register it in the DB
    kaisai_dates = date_module.load_dates(year, month)
    #Load race result and register it in the DB from kaisai date results
    race_result_module.load_race_results(kaisai_dates)
    # race_result_module.load_race_results()

    print("終了")
