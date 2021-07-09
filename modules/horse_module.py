import time
from config import const
from config import class_const
from config import urls
from utils import selenium_util
from utils import re_util
from scraping import html_parser
from data import horse
from data import race_result


def get_horse_id_from_result():
    """
    keiba_db.race_resultsからkeiba_db.horsesコレクションに存在しない競走馬ID一覧を返却する。

    Returns
    -------
    horse_ids:list of str
        keiba_db.horsesに存在しない競走馬ID一覧
    """
    horse_ids = race_result.get_horse_ids()
    return horse.get_not_exist_ids(horse_ids)

def register_horses(horse_ids):
    """
    レース結果一覧から競走馬情報を登録する。

    Parameters
    ----------
    horse_ids:list of str
        競走馬ID一覧
    """
    data = []
    for horse_id in horse_ids:
        url = urls.DATABASE_URL + "horse/" + horse_id
        html_text = selenium_util.get_page(url)
        time.sleep(const.INTERVAL_TIME)

        title_element = html_parser.get_from_text(html_text, "div", class_const.HORSE_INFO_TITLE_CLASS)
        horse_name = title_element.find("h1").text.replace("○外", "")
        horse_info = {"horse_id": horse_id, "horse_name": horse_name.strip()}

        horse_data = html_parser.get_from_text(html_text, "table", class_const.HORSE_PROFILE_TABLE_CLASS).find_all("tr")
        horse_info["birthday"] = horse_data[0].find("td").text
        a = horse_data[1].find("a")
        horse_info["stable_id"] = re_util.get_from_text(const.STABLE_ID_PATTERN, a.attrs['href'])

        a = horse_data[2].find("a")
        horse_info["owner_id"] = re_util.get_from_text(const.OWNER_ID_PATTERN, a.attrs['href'])

        a = horse_data[4 if len(horse_data[3].attrs) != 0 and horse_data[3].attrs['id'] == "owner_info_tr" else 3].find("a")
        horse_info["farm_id"] = re_util.get_from_text(const.FARM_ID_PATTERN, a.attrs['href'])

        blood_data = html_parser.get_from_text(html_text, "table", class_const.HORSE_BLOOD_TABLE_CLASS).find_all("tr")
        a = blood_data[0].find("a")
        horse_info["father_id"] = re_util.get_from_text(const.BLOOD_ID_PATTERN, a.attrs['href'])
        a = blood_data[3].find("a")
        horse_info["mother_id"] = re_util.get_from_text(const.BLOOD_ID_PATTERN, a.attrs['href'])
        data.append(horse_info)

    selenium_util.close_chrome()
    horse.insert(data)
