import requests
import traceback
from config import const

def request_get(url):
    try:
        responce = requests.get(url, headers=const.HTTP_HEADER)
        responce.encoding = responce.apparent_encoding
        return responce.text
    except:
        traceback.print_exc()
        return None
