from config import const
from config import urls
from config import class_const
from utils import re_util
from utils import url_connect
from scraping import html_parser
from data import kaisai_date
import datetime


def load_dates(year, month):
    """
    年、月からURLを参照してスクレイピングを行い開催の一覧を返却する。
    private

    Parameters
    ----------
    year:int
        取得する年
    month:int
        取得する月

    Returns
    -------
    date_info:list of dict
        開催データ一覧
    """
    date_info = []
    url = urls.RACE_URL + "top/calendar.html?year=" + str(year) + "&month=" + str(month)
    html_text = url_connect.request_get(url)
    calendar = html_parser.get_from_text(html_text, "table", class_const.CALENDAR_TABLE_CLASS)
    dates = html_parser.get_elements(calendar, "td", class_const.DATE_CELL_BOX_CLASS)
    for date in dates:
        a = date.find("a")
        if a == None:
            continue
        href = a.attrs['href']
        kaisai_id = re_util.get_from_text(const.DATE_URL_PATTERN, href)
        courses = html_parser.get_elements(a, "span", "JyoName")
        for course in courses:
            date_string = kaisai_id[0:4] + "-" + kaisai_id[4:6] + "-" + kaisai_id[6:8]
            date_info.append({"date": date_string, "kaisai_id": kaisai_id, "course_name": course.text})
    return date_info

def register_dates():
    """
    実行日の６月から実行月までの開催データを取得してDBに登録する

    Returns
    -------
    data:list of dict
        新規で挿入したkeiba_db.datesコレクションのリスト
    """
    today = datetime.date.today()
    years = [today.year]
    if today.month < 4:
        years.append(today.year - 1)

    data = []
    for year in years:
        months = [1, 2, 3] if year == today.year and today.month < 4 else [6, 7, 8, 9, 10, 11, 12]
        for month in months:
            if month > today.month:
                break
            data.extend(load_dates(year, month))
    insert_data = kaisai_date.insert_dates(data)
    return insert_data
