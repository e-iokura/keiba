import const
import urls
import db_config
import class_const

def set_const_values():
    urls.DATABASE_URL = "https://db.netkeiba.com/"
    urls.RACE_URL = "https://race.netkeiba.com/"

    const.HTTP_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    const.DATE_URL_PATTERN = "\/top\/race_list.html\?kaisai_date=(.*)$"
    const.RACE_LIST_PATTERN = "\/race\/result.html\?race_id=(.*)&amp;rf=race_list"
    const.GRADE_CLASS_PATTERN = "Icon_GradeType[0-9]+"
    const.INTERVAL_TIME = 3

    class_const.PICKUP_RACE_BOX_CLASS = "Jra_RaceList_Inner RaceInfo"
    class_const.SUB_PICKUP_RACE_BOX_CLASS = "RaceMostRecentBox"
    class_const.RACE_RESULT_TABLE_CLASS = "race_table_01 nk_tb_common"
    class_const.CALENDAR_TABLE_CLASS = "Calendar_Table"
    class_const.DATE_CELL_BOX_CLASS = "RaceCellBox"
    class_const.RACE_LIST_ITEM_CLASS = "RaceList_DataItem"
    class_const.OPEN_GRADE_CLASS_LIST = ["Icon_GradeType1", "Icon_GradeType2", \
        "Icon_GradeType3""Icon_GradeType15", "Icon_GradeType5"]
    class_const.RACE_LIST_ITEM_TITLE_CLASS = "RaceList_ItemTitle"

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
