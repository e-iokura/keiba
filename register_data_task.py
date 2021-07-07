from config import app_setting
from modules import date_module
from modules import race_module
from modules import race_result_module

if __name__ == '__main__':
    app_setting.set_const_values()

    #Load the date of this month and register it in the DB
    kaisai_dates = date_module.register_dates()
    #Load race list from kaisai dates results
    races = race_module.load_races(kaisai_dates)
    #Load race result and register it in the DB from race list results
    race_result_module.register_race_result(races)

    print("終了")
