from HTML_Scraper import *
from debugging import *
import urllib

# DATA ACCESSORS
def make_default_form_data():
    return make_form_data(None)

def make_form_data(values: dict):
    result = {'EndTime': '', 'CourseCodes': '', 'ShowComments': '', 'Room': '', 'InstrName': '', 'YearTerm': '2017-03', 'MaxCap': '', 'ShowFinals': '', 'StartTime': '', 'Dept': 'CSE', 'Bldg': '', 'Breadth': 'ANY', 'FullCourses': '', 'CourseNum': '', 'Division': 'ANY', 'Days': '', 'ClassType': 'ALL', 'FontSize': '100', 'Units': '', 'CourseTitle': '', 'CancelledCourses': 'Exclude'}

    if(values != None):
        for key in values:
            result[key] = values[key]

    return result

def get_classes(form_data):
    classes_tree = HTMLTree()
    classes_tree.get_HTML_from_string(_get_class_data(form_data))
    classes_tree.parse_data()
    results = classes_tree.find_nodes_by_attribute("valign", "top")
    return results

def _get_class_data(form_data):
    url = "https://www.reg.uci.edu/perl/WebSoc/"
    params = urllib.parse.urlencode(form_data).encode('UTF-8')
    request = urllib.request.Request(url, params)
    return urllib.request.urlopen(request).read().decode('utf-8')

def get_pippins_food():
    return _get_food_items("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=4832")

def get_anteatery_food():
    return _get_food_items("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3056")

def get_brandy_food():
    return _get_food_items("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3078")

def _get_food_items(url):
    food_tree = HTMLTree()
    food_tree.get_HTML_from_url(url)
    food_tree.parse_data()
    results = food_tree.find_nodes_by_attribute("rel", "prettyPhotoiFrameWithoutNavigation")
    return results

#selected date = (class = "menu-date selected")
#other dates = (class = "menu-sate")
#menu perios = (class = "menu-period")
#expand all button = ( class = "txt-button left-spacem")
#headers = (class = "collapsible-header")
# items = (rel = "prettyPhotoiFrameWithoutNavigation")
#nutrition = (id = "WebPartManager1_wpMenuItemDetails)
