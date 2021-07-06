from config import app_setting
from config import const
from config import urls
from config import class_const
import csv
import datetime
import time
from utils import selenium_util
from utils import re_util
from scraping import html_parser
from data import race as race_collection
from data import race_result

def load_race_results(kaisai_dates):
    dates = []
    info = []
    today = datetime.date.today()
    age = 2 if today.month >= 6 and today.month <= 12 else 3
    except_titles = ["4歳"]
    if age == 2:
        except_titles.append("3歳")
    for kaisai_date in kaisai_dates:
        split_date = kaisai_date['date'].split("-")
        date = datetime.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        if date >= today:
            continue

        if dates.__contains__(kaisai_date['kaisai_id']):
            continue
        dates.append(kaisai_date['kaisai_id'])
        time.sleep(const.INTERVAL_TIME)

        url = urls.RACE_URL + "top/race_list.html?kaisai_date=" + kaisai_date['kaisai_id']
        html_text = selenium_util.get_page(url)

        elements = html_parser.get_all_from_text(html_text, "li", class_const.RACE_LIST_ITEM_CLASS)
        for element in elements:
            title_element = html_parser.get_element(element, "div", class_const.RACE_LIST_ITEM_TITLE_CLASS)
            title_children = []
            for child in title_element.contents:
                if child != "\n":
                    title_children.append(child)
            race_name = title_children[0].text
            is_exclusion = False
            for except_title in except_titles:
                if except_title in race_name:
                    is_exclusion = True
                    break
            if is_exclusion:
                continue

            grade_type_class = title_children[1].attrs['class'] if len(title_children) == 2 else race_name
            grade_type = re_util.get_from_text(const.GRADE_CLASS_PATTERN, grade_type_class[1]) if len(title_children) == 2 else race_name
            a = element.find("a")
            href = a.attrs['href']
            race_id = re_util.get_from_text(const.RACE_LIST_PATTERN, href)
            grade = app_setting.get_grade_name(grade_type)
            info.append({"race_id":race_id,"kaisai_id":kaisai_date['kaisai_id'],"race_name":race_name,"grade":grade})

    with open('C:/dev/python/keiba/csv/race_list.csv', 'w', encoding='utf-8_sig') as f:
        writer = csv.DictWriter(f, fieldnames=["race_id","kaisai_id","race_name","grade"])
        writer.writeheader()
        for row in info:
            writer.writerow(row)
    insert_race_result(info)


# def load_race_results():
#     csv_header = ["race_id", "kaisai_id", "race_name", "grade"]
#     info = []
#     with open('C:/dev/python/keiba/csv/race_list.csv', 'r', encoding="utf-8_sig") as f:
#         reader = csv.DictReader(f, csv_header)
#         reader.__next__()
#         for row in reader:
#             info.append(row)
#     insert_race_result(info)


def insert_race_result(races):
    today = datetime.date.today()
    age = "２歳" if today.month >= 6 and today.month <= 12 else "３歳"
    info = []
    for race in races:
        time.sleep(const.INTERVAL_TIME)
        url = urls.RACE_URL + "race/result.html?race_id=" + race['race_id']
        html_text = selenium_util.get_page(url)
        race_info_element = html_parser.get_from_text(html_text, "div", class_const.RACE_INFO_BOX_CLASS)
        race_data = html_parser.get_element(race_info_element, "div", "RaceData02").find_all("span")
        race_gen = race_data[3].text
        if age not in race_gen:
            continue

        race_num = html_parser.get_element(race_info_element, "span", "RaceNum").text
        head_count = race_data[7].text
        race['race_num'] = race_num
        race['head_count'] = head_count
        race_collection.insert(race)

        rows = html_parser.get_all_from_text(html_text, "tr", class_const.RACE_RESULT_ROW_LIST_CLASS)
        for row in rows:
            horse_info = html_parser.get_element(row, "td", "Horse_Info")
            a = horse_info.find("a")
            horse_id = re_util.get_from_text(const.HORSE_ID_PATTERN, a.attrs['href'])
            jockey_info = html_parser.get_element(row, "td", "Jockey")
            a = jockey_info.find("a")
            jockey_id = re_util.get_from_text(const.JOCKEY_ID_PATTERN, a.attrs['href'])
            cols = row.find_all("td")
            info.append({"race_id": race['race_id'], "horse_id": horse_id, "jockey_id": jockey_id, "rank": trim(cols[0]), "waku": trim(cols[1]), "umaban": trim(cols[2]),
                         "jockey_weight": trim(cols[5]), "time": trim(cols[7]), "passing_order": trim(cols[10]), "last_3f": trim(cols[11]), "horse_weight": trim(cols[14]),
                         "win_odds": trim(cols[12]), "popular_order": trim(cols[13])})
    race_result.insert_data(info)
    selenium_util.close_chrome()

def trim(bs_element):
    return re_util.trim_bs_text(bs_element.text)
