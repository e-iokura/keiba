from config import app_setting
from config import const
from config import urls
from config import class_const
import datetime
import time
from utils import selenium_util
from utils import re_util
from scraping import html_parser
from data import race
from data import kaisai_date


def parse_dates(kaisai_dates):
    """
    開催データ一覧から開催日の重複を削除してdatetimeの値を付加したリストを返却する
    private

    Parameters
    ----------
    kaisai_dates:list of dict
        keiba_db.datesコレクションのリスト

    Returns
    -------
    dates:list of dict
        keiba_db.datesコレクションのリストから開催日の重複をなくしてdatetimeの値を付加したリスト
    """
    dates = []
    for kaisai_date in kaisai_dates:
        if dates.__contains__(kaisai_date['kaisai_id']):
            continue
        split_date = kaisai_date['date'].split("-")
        date = datetime.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        kaisai_date['date_info'] = date
        dates.append(kaisai_date)
    return dates


def load_races(kaisai_dates):
    """
    開催データ一覧からレース情報一覧をスクレイピングして返却する。

    Parameters
    ----------
    kaisai_dates:list of dict
        開催データ一覧

    Returns
    -------
    not_exist_data:list of dict
        DBに存在しないレース情報一覧
    """
    dates = parse_dates(kaisai_dates)
    data = []
    today = datetime.date.today()
    except_titles = ["4歳"]
    if today.month >= 6 and today.month <= 12 == 2:
        except_titles.append("3歳")
    for kaisai_date in dates:
        if kaisai_date['date_info'] >= today:
            continue

        url = urls.RACE_URL + "top/race_list.html?kaisai_date=" + kaisai_date['kaisai_id']
        html_text = selenium_util.get_page(url)
        time.sleep(const.INTERVAL_TIME)

        elements = html_parser.get_all_from_text(html_text, "li", class_const.RACE_LIST_ITEM_CLASS)
        for element in elements:
            title_element = html_parser.get_element(element, "div", class_const.RACE_LIST_ITEM_TITLE_CLASS)
            title_children = [child for child in title_element.contents if child != "\n"]
            race_name = title_children[0].text
            if True in [title in race_name for title in except_titles]:
                continue

            grade_type = re_util.get_from_text(const.GRADE_CLASS_PATTERN, title_children[1].attrs['class'][1]) if len(title_children) == 2 else race_name
            grade = app_setting.get_grade_name(grade_type)
            a = element.find("a")
            race_id = re_util.get_from_text(const.RACE_LIST_PATTERN, a.attrs['href'])
            data.append({"race_id": race_id, "kaisai_id": kaisai_date['kaisai_id'], "race_name": race_name, "grade": grade})
    selenium_util.close_chrome()
    not_exist_data = race.get_not_exist_data(data)
    return not_exist_data


def load_races_from_dates():
    kaisai_dates = kaisai_date.get_dates()
    return load_races(kaisai_dates)
