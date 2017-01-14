from HTML_Scraper import *
import urllib



def send_form(url, form_data):
    params = urllib.parse.urlencode(form_data)
    print(params)
    request = urllib.request.Request(url, params)
    return request

print(send_form("https://www.reg.uci.edu/perl/WebSoc", {'spam': 1, 'eggs': 2, 'bacon': 0}))
    
names = ['YearTerm', 'ShowComments', 'ShowFinals',
         'Breadth', 'Dept', 'CourseNum', 'Division',
         'CourseCodes', 'InstrName', 'CourseTitle',
         'ClassType', 'Units', 'Days', 'StartTime',
         'EndTime', 'MaxCap', 'FullCourses',
         'FontSize', 'CancelledCourses', 'Bldg',
         'Room']
         

#selected date = (class = "menu-date selected")
#other dates = (class = "menu-sate")
#menu perios = (class = "menu-period")
#expand all button = ( class = "txt-button left-spacem")
#headers = (class = "collapsible-header")
# items = (rel = "prettyPhotoiFrameWithoutNavigation")
#nutrition = (id = "WebPartManager1_wpMenuItemDetails)
