import bs4
import traceback

def get_from_text(html_text, tag, class_name = None):
    try:
        bs = bs4.BeautifulSoup(html_text, 'html.parser')
        return bs.find(tag, class_=class_name) \
            if class_name != None else bs.find(tag)
    except:
        traceback.print_exc()
        return None

def get_element(parent, tag, class_name=None):
    return parent.find(tag, class_=class_name) \
        if class_name != None else parent.find(tag)

def get_elements(parent, tag, class_name=None):
    return parent.find_all(tag, class_=class_name) \
        if class_name != None else parent.find_all(tag)
