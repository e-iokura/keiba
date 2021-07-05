from config import app_setting
from config import const
from config import urls
from config import class_const
import time
from utils import re_util
from utils import url_connect
from scraping import html_parser

def load_rece_results(kaisai_dates):
    dates = []
    info = []
    for kaisai_date in kaisai_dates:
        if dates.__contains__(kaisai_date['kaisai_id']):
            continue
        dates.append(kaisai_date['kaisai_id'])
        url = urls.RACE_URL + "top/race_list.html?kaisai_date=" + kaisai_date['kaisai_id']
        html_text = url_connect.request_get(url)

        elements = html_parser.get_from_text(html_text, "li", class_=class_const.RACE_LIST_ITEM_CLASS)
        for element in elements:
            title_element = html_parser.get_elements(element, "div", class_const.RACE_LIST_ITEM_TITLE_CLASS)
            if title_element == None or len(title_element) != 2:
                continue
            race_name = title_element[0].text
            grade_type_class = title_element[1].attr['class']
            grade_type = re_util.get_from_text(const.GRADE_CLASS_PATTERN, grade_type_class)
            a = element.find("a")
            if grade_type == "" or grade_type not in class_const.OPEN_GRADE_CLASS_LIST or a == None:
                continue
            href = a.attrs['href']
            race_id = re_util.get_from_text(const.RACE_LIST_PATTERN, href)
            grade = app_setting.get_grade_name(grade_type)
            info.append({"race_id":race_id,"race_name":race_name,"grade":grade})

        time.sleep(const.INTERVAL_TIME)

def insert_race_result(race_id):
    url = urls.DATABASE_URL + "race/" + race_id
    html_text = url_connect.request_get(url)
    result_table = html_parser.get_from_text(html_text, class_const.RACE_RESULT_TABLE_CLASS)
    info = []
    rows = result_table.find_all("tr")
