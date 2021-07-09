from config import app_setting
from modules import date_module
from modules import race_module
from modules import race_result_module


def register_data():
    """
    開催データ→レース一覧→レース結果の順にスクレイピングしてデータをDBに登録する。
    """
    #Load the date of this month and register it in the DB
    kaisai_dates = date_module.register_dates()
    #Load race list from kaisai dates results
    races = race_module.load_races(kaisai_dates)
    #Load race result and register it in the DB from race list results
    race_result_module.register_race_result(races)


def register_race():
    """
    keiba_db.datesコレクションから開催データ一覧を取得しレース情報、レース結果をスクレイピングしてDBに登録する。
    """
    #Load the date of this month and register it in the DB
    #Load race list from kaisai dates results
    races = race_module.load_races_from_dates()
    #Load race result and register it in the DB from race list results
    race_result_module.register_race_result(races)

if __name__ == '__main__':
    app_setting.set_const_values()

    register_race()

    print("終了")
