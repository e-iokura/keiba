from config import const
from config import urls
from config import class_const
import datetime
import time
from utils import selenium_util
from utils import re_util
from scraping import html_parser
from data import race as race_collection
from data import race_result

def trim(bs_element):
    return bs_element.text.replace("\n", "").strip()

def register_race(html_text, race):
    """
    レース情報をスクレイピングしてkeiba_db.racesコレクションに挿入する。
    private

    Parameters
    ----------
    html_text:str
        URL参照先のHTML
    race:dict in one element
        レース情報

    Returns
    -------
    age_info:str
        レース馬齢情報
    """
    race_info_element = html_parser.get_from_text(html_text, "div", class_const.RACE_INFO_BOX_CLASS)
    race_data1 = html_parser.get_element(race_info_element, "div", "RaceData01").find_all("span")
    race_data2 = html_parser.get_element(race_info_element, "div", "RaceData02").find_all("span")

    race_num = html_parser.get_element(race_info_element, "span", "RaceNum").text
    race_name = html_parser.get_element(race_info_element, "div", "RaceName")
    race['race_name'] = trim(race_name)
    race['race_num'] = race_num
    race['course_name'] = race_data2[1].text
    race['distance'] = race_data1[0].text
    race['head_count'] = race_data2[7].text
    race_collection.insert(race)
    return race_data2[3].text

def register_race_result(races):
    """
    レース一覧からレース結果をスクレイピングしてkeiba_db.race_resultsに挿入する。

    Parameters
    ----------
    races:list of dict
        レース情報一覧
    """
    today = datetime.date.today()
    data = []
    age = "２歳" if today.month >= 6 and today.month <= 12 else "３歳"
    for race in races:
        if("2歳" in race['race_name']):
            continue
        url = urls.RACE_URL + "race/result.html?race_id=" + race['race_id']
        html_text = selenium_util.get_page(url)
        time.sleep(const.INTERVAL_TIME)

        age_info = register_race(html_text, race)
        if age in age_info:
            continue

        rows = html_parser.get_all_from_text(html_text, "tr", class_const.RACE_RESULT_ROW_LIST_CLASS)
        for row in rows:
            a = html_parser.get_element(row, "td", "Horse_Info").find("a")
            horse_id = re_util.get_from_text(const.HORSE_ID_PATTERN, a.attrs['href'])
            a = html_parser.get_element(row, "td", "Jockey").find("a")
            jockey_id = re_util.get_from_text(const.JOCKEY_ID_PATTERN, a.attrs['href'])
            cols = row.find_all("td")
            data.append({"race_id": race['race_id'], "horse_id": horse_id, "jockey_id": jockey_id, "rank": trim(cols[0]), "waku": trim(cols[1]), "umaban": trim(cols[2]),
                         "hourse_age": trim(cols[4]), "jockey_weight": trim(cols[5]), "time": trim(cols[7]), "passing_order": trim(cols[12]), "last_3f": trim(cols[10]),
                          "horse_weight": trim(cols[14])})
    race_result.insert_data(data)
    selenium_util.close_chrome()
