from config import const
from config import urls
from config import db_config
from config import class_const

def set_const_values():
    """
    アプリケーションで使用される定数値を設定する。

    Notes
    -----
    各定数値モジュールに定数を設定する
    1. urls:使用するURLモジュール
    2. const:アプリケーション定数モジュール
    3. class_const:スクレイピングで使用するクラス名モジュール
    4. db_config:接続DB設定値モジュール
    """
    urls.DATABASE_URL = "https://db.netkeiba.com/"
    urls.RACE_URL = "https://race.netkeiba.com/"

    const.HTTP_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    const.DATE_URL_PATTERN = "\/top\/race_list.html\?kaisai_date=(.*)$"
    const.RACE_LIST_PATTERN = "\/race\/result.html\?race_id=(.*)&rf=race_list"
    const.HORSE_ID_PATTERN = "\/horse\/(.*)$"
    const.JOCKEY_ID_PATTERN = "\/jockey\/(.*)\/"
    const.GRADE_CLASS_PATTERN = "Icon_GradeType[0-9]+"
    const.INTERVAL_TIME = 5
    const.CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"

    class_const.PICKUP_RACE_BOX_CLASS = "Jra_RaceList_Inner RaceInfo"
    class_const.SUB_PICKUP_RACE_BOX_CLASS = "RaceMostRecentBox"
    class_const.RACE_RESULT_ROW_LIST_CLASS = "HorseList"
    class_const.CALENDAR_TABLE_CLASS = "Calendar_Table"
    class_const.DATE_CELL_BOX_CLASS = "RaceCellBox"
    class_const.RACE_LIST_ITEM_CLASS = "RaceList_DataItem"
    class_const.OPEN_GRADE_CLASS_LIST = ["Icon_GradeType1", "Icon_GradeType2", "Icon_GradeType3""Icon_GradeType15", "Icon_GradeType5", \
        "Icon_GradeType16", "Icon_GradeType17", "Icon_GradeType18"]
    class_const.RACE_LIST_ITEM_TITLE_CLASS = "RaceList_ItemTitle"
    class_const.RACE_INFO_BOX_CLASS = "RaceList_NameBox"

    db_config.DB_HOST = "mongodb://127.0.0.1:27017/"
    db_config.DB_USER_NAME = "keiba"
    db_config.DB_PASSWORD = "keiba123"


def get_grade_name(grade_type):
    if grade_type == "Icon_GradeType1":
        return "G1"
    if grade_type == "Icon_GradeType2":
        return "G2"
    if grade_type == "Icon_GradeType3":
        return "G3"
    if grade_type == "Icon_GradeType15":
        return "Listed"
    if grade_type == "Icon_GradeType5":
        return "Open"
    if grade_type == "Icon_GradeType16":
        return "3勝クラス"
    if grade_type == "Icon_GradeType17" or "2勝" in grade_type:
        return "2勝クラス"
    if grade_type == "Icon_GradeType18" or "1勝" in grade_type:
        return "1勝クラス"
    if "未勝利" in grade_type:
        return "未勝利"
    if "メイクデビュー" in grade_type or "新馬" in grade_type:
        return "新馬"
    return ""
