from config import const
from config import urls
from config import class_const
from utils import re_util
from utils import url_connect
from scraping import html_parser
from data import kaisai_date

def load_dates(year, month):
    url = urls.RACE_URL + "top/calendar.html?year=" + str(year) + "&month=" + str(month)
    html_text = url_connect.request_get(url)
    calendar = html_parser.get_from_text(html_text, "table", class_const.CALENDAR_TABLE_CLASS)
    dates = html_parser.get_elements(calendar, "td", class_const.DATE_CELL_BOX_CLASS)
    data = []
    for date in dates:
        a = date.find("a")
        if a == None:
            continue
        href = a.attrs['href']
        kaisai_id = re_util.get_from_text(const.DATE_URL_PATTERN, href)
        courses = html_parser.get_elements(a, "span", "JyoName")
        for course in courses:
            date_string = kaisai_id[0:4] + "-" + kaisai_id[4:6] + "-" + kaisai_id[6:8]
            data.append({"date":date_string,"kaisai_id":kaisai_id,"course_name":course.text})
    kaisai_date.insert_dates(data)
    return data
