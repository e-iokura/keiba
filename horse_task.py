from config import app_setting
from modules import horse_module

def register_from_race_results():
    """
    keiba_db.horsesコレクションから競走馬一覧を取得して競走馬データをDBに登録する。
    """
    #Load horse and register it in the DB from race result list
    horse_ids = horse_module.get_horse_id_from_result()
    horse_module.register_horses(horse_ids)

if __name__ == '__main__':
    app_setting.set_const_values()

    register_from_race_results()

    print("終了")
