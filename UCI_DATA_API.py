from OneHack_HTML_Parser import *
from UDA_debugging import *
from OneHack_HTML_Parser import NodeType
from urllib.parse import urlparse
import json

UCI_URLs = {"webreg" : "https://www.reg.uci.edu/perl/WebSoc/", "brandy" : "https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3078", "pippins" : "https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=4832", "anteater" : "https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3056" }

class RetrievalFailure(Exception):
    """ Indicates a failure to get html data  from a source"""
    pass

class BadURLException(Exception):
    """ Indicates a failure to detect a valid url"""
    pass

class UCI_DATA_BASE:
    def __init__(self, strict=False, encoding="utf-8"):
        self._HTML_Tree = ReferencedHTMLTree()
        self._data_source = ""

        self._encoding = "utf-8"

        self._strict = strict

        self._processed_data = {}

    def reset(self) -> None:
        self._HTML_Tree.reset_data_struct()
        self._data_source = ""

        self._processed_data = {}

    def getJSON(self) -> str:
        return json.dumps(self._processed_data)

    def get_result(self):
        return self._processed_data

    def set_html_target(self, path:str) -> None:
        if(urlparse(path).scheme != "" and urlparse(path).netloc != "" and (not self._strict or path in UCI_URLs.values())):
            self._data_source = path
            self._HTML_Tree.get_HTML_from_url(self._data_source)
        else:
            raise BadURLException("The given path is not identified as a valid URL: " + path)

    def process_available_data(self) -> bool:
        if(self._data_source != ""):
            self._HTML_Tree.parse_data()

    def process_result(self):
        pass

class ClassDataManager(UCI_DATA_BASE):
    def __init__(self):
        self._form_data = {}

        super(ClassDataManager, self).__init__()

        self._make_default_form_data()

    def process_result(self):
        attribute_order = ("code", "type", "sec", "units", "instructor", "time", "place", "max", "enr", "wl", "req", "rstr", "textbooks", "web", "status")

        table = self._HTML_Tree.find_nodes_by_attribute("class", "college-title", short=True)[0].get_parent()

        totalLength = len(table.get_children())

        result = {}

        rowNum = 0
        currentCourse = ""
        currentResult = {}

        for i, child in enumerate(table.get_children()):
            debug_print(str(i) + " / " + str(totalLength))
            if(child.get_attribute("class") in ["blue-bar"]):
                result[currentCourse] = currentResult
                rowNum = 0
                currentResult = {}
                currentCourse = ""
                continue
            elif(child.get_attribute("class") in ["college-title", "dept-title"]):
                continue
            elif(rowNum % 2 == 0 and child.get_type() != NodeType.data): # data row
                if(child.get_children()[0].get_attribute("class") == "CourseTitle"):
                    templi = child.get_children()[0].get_children()[0].get_data().split(" ")
                    currentCourse = templi[0] + " " + templi[len(templi)-1]
                else:
                    for n, attribute in enumerate(child.get_children()):
                        if(attribute.get_children() == []):
                            currentResult[attribute_order[n]] = ""
                        else:
                            currentResult[attribute_order[n]] = attribute.get_children()[0].get_data()
            rowNum += 1

        self._processed_data = result

    def reset(self) -> None:
        self._make_default_form_data()
        super(ClassDataManager, self).reset()

    def _make_default_form_data(self):
        self._form_data = {'EndTime': '', 'CourseCodes': '', 'ShowComments': '', 'Room': '', 'InstrName': '', 'YearTerm': '2017-03', 'MaxCap': '', 'ShowFinals': '', 'StartTime': '', 'Dept': 'CSE', 'Bldg': '', 'Breadth': 'ANY', 'FullCourses': '', 'CourseNum': '', 'Division': 'ANY', 'Days': '', 'ClassType': 'ALL', 'FontSize': '100', 'Units': '', 'CourseTitle': '', 'CancelledCourses': 'Exclude'}

    def update_data(self, key: str, value: str):
        if(key in self._form_data):
            self._form_data[key] = value

    def set_html_target(self, path=None):
        if(path):
            super(ClassDataManager, self).set_html_target(path)
        else:
            debug_print("Preparing Tree-Parser: " + str(self._HTML_Tree))
            self._HTML_Tree.get_HTML_from_string(self._get_class_data())
            self._data_source = "POST Query"

    def _get_class_data(self):
        url = UCI_URLs["webreg"]
        params = urllib.parse.urlencode(self._form_data).encode(self._encoding)
        request = urllib.request.Request(url, params)
        return urllib.request.urlopen(request).read().decode('utf-8')

class FoodDataManager(UCI_DATA_BASE):
    def __init__(self):
        super(FoodDataManager, self).__init__()

    def process_result(self):
        foods = self._HTML_Tree.find_nodes_by_attribute("rel", "prettyPhotoiFrameWithoutNavigation")
        secondaryParser = ReferencedHTMLTree()

        result = {}

        for food in foods:
            foodInfo = food.get_attribute("data-content")

            secondaryParser.reset_data_struct()
            secondaryParser.get_HTML_from_string(foodInfo)
            secondaryParser.parse_data()

            details = secondaryParser.find_nodes_by_attribute("class", "menu-item")[0]

            result[details.find_child("class", "title", recursive = True).get_children()[0].get_data()] = details.find_child("class", "description", recursive = True).get_children()[0].get_data()

        self._processed_data = result


    def get_pippins_food(self):
        return self.__get_food_items(UCI_URLs["pippins"])

    def get_anteatery_food(self):
        return self.__get_food_items(UCI_URLs["anteater"])

    def get_brandy_food(self):
        return self.__get_food_items(UCI_URLs["brandy"])

    def __get_food_items(self, url):
        self.set_html_target(url)

if __name__ == '__main__':
    if(input("Test [CLASSES/FOOD]? ").lower() == "classes"):
        print("STARTING TESTS")
        courseManager = ClassDataManager()
        print("SETTING HTML")
        courseManager.set_html_target()
        print("Processing Data")
        courseManager.process_available_data()
        print("Finalizing Answer")
        courseManager.process_result()
        print("Printing JSON")
        print(courseManager.getJSON())
    else:
        print("STARTING TESTS")
        foodManager = FoodDataManager()

        test = input("[pippins/brandy/anteater]? ").lower()
        print("Processing food")
        if(test == "pippins"):
            foodManager.get_pippins_food()
        elif(test == "brandy"):
            foodManager.get_brandy_food()
        else:
            foodManager.get_anteatery_food()

        print("Processing Data")
        foodManager.process_available_data()
        print("Finalizing Answer")
        foodManager.process_result()
        print("Printing JSON")
        print(foodManager.getJSON())
