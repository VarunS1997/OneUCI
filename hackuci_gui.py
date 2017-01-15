import tkinter as tk
from UDA_debugging import *
from UCI_DATA_API import *
from datetime import date

def get_dimmensions():
    dimmensions = {}
    dimmensions["navigation"] = (80, 80)
    dimmensions["banner"] = (400, 40)
    dimmensions["food"] = (400, 120)
    dimmensions["class"] = (400, 60)
    dimmensions["event"] = (400, 40)
    return dimmensions

class GUI:
    def __init__(self, DISPLAY_WIDTH = 400, DISPLAY_HEIGHT = 640, PRIMARY_COLOR = "#00255D", SECONDARY_COLOR = "#FFD200"):
        self.__PRIMARY_COLOR = PRIMARY_COLOR
        self.__SECONDARY_COLOR = SECONDARY_COLOR

        self.__DISPLAY_WIDTH = DISPLAY_WIDTH
        self.__DISPLAY_HEIGHT = DISPLAY_HEIGHT

        self.__DIMMENSIONS = get_dimmensions()

        self.__buttons = []
        self.__course_buttons = []
        self.__button_images = []
        self.__current_button = 3
        self.__xorigin = 0
        self.__yorigin = 0
        self.__tile_margins = 10
        self.__FOOD_COUNT = 0
        self.__FOOD_PERIOD = 0
        self.__DAY_COUNT = 0

        self.__current_icon = 10

        self.__top = tk.Tk()

        self.__icons = [tk.PhotoImage(file='icons/uci_maps.gif'),
                tk.PhotoImage(file='icons/uci_food.gif'),
                tk.PhotoImage(file='icons/uci_planner.gif'),
                tk.PhotoImage(file='icons/uci_webreg.gif'),
                tk.PhotoImage(file='icons/uci_events.gif'),
                tk.PhotoImage(file='icons/uci_maps_selected.gif'),
                tk.PhotoImage(file='icons/uci_food_selected.gif'),
                tk.PhotoImage(file='icons/uci_planner_selected.gif'),
                tk.PhotoImage(file='icons/uci_webreg_selected.gif'),
                tk.PhotoImage(file='icons/uci_events_selected.gif'),
                tk.PhotoImage(file='icons/map_img.gif'),
                tk.PhotoImage(file='icons/HH_map.gif'),
                tk.PhotoImage(file='icons/ELH_map.gif'),
                tk.PhotoImage(file='icons/HSLH_map.gif'),
                tk.PhotoImage(file='icons/ICS_map.gif')]

        self.__title_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DIMMENSIONS["banner"][1]*2)
        self.__title_canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__title_canvas.bind('<Configure>', self.draw_title)

        self.__content_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DISPLAY_HEIGHT-self.__DIMMENSIONS["banner"][1]*2-self.__DIMMENSIONS["navigation"][1])
        self.__content_canvas.grid(row = 1, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__content_canvas.bind('<Button-1>', self.__content_click)
        self.__content_canvas.bind('<B1-Motion>', self.__scroll_scrollables)
        self.__content_canvas.bind('<Motion>', self.__set_scroll_last)
        self.__content_canvas.bind('<Configure>', self.draw_content)

        self.__nav_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DIMMENSIONS["navigation"][1], cursor='hand2')
        self.__nav_canvas.grid(row = 2, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__nav_canvas.bind('<Button-1>', self.handle_radio)
        self.__nav_canvas.bind('<Configure>', self.draw_menu)

        self.pip_breakfast = {}
        self.pip_lunch = {}
        self.pip_dinner = {}
        self.brand_lunch = {}
        self.brand_dinner = {}
        self.ant_breakFast = {}
        self.ant_lunch = {}
        self.ant_dinner = {}

        self.__entry_fields = ["Dept", "CourseNum"]
        self.__entry_vars = []
        for field in self.__entry_fields:
            var = tk.StringVar()
            var.set("")
            self.__entry_vars.append(var)
        self.__entry_vars[0].set("I&C SCI")
        self.__classDataManager = None
        self.__submit_button = None

        self.__classes = ["CS 122B: 11:00-12:20 @ HSLH 100A", "CS 162: 12:30-1:50 @ ICS 174", "GEN&SEX 40B: 2:00-3:20 @ ELH 100", "CS 167: 3:30-4:50 @ HH 178"]
        self.__events = ["HACK UCI ALL DAY EVERY DAY", "122B PROJECT 1 DUE WED 11:55PM"]
        self.__classData = {}

        self.__days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']

    def run(self):
        self.__top.mainloop()

    def initialize_data(self):
        foodDataManager = FoodDataManager()

        foodDataManager.get_pippins_food('breakfast')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.pip_breakfast = foodDataManager.get_result()

        foodDataManager.get_pippins_food('lunch')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.pip_lunch = foodDataManager.get_result()

        foodDataManager.get_pippins_food('dinner')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.pip_dinner = foodDataManager.get_result()

        foodDataManager.get_brandy_food('breakfast')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.brand_breakfast = foodDataManager.get_result()

        foodDataManager.get_brandy_food('lunch')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.brand_lunch = foodDataManager.get_result()

        foodDataManager.get_brandy_food('dinner')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.brand_dinner = foodDataManager.get_result()

        foodDataManager.get_anteatery_food('breakfast')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.ant_breakfast = foodDataManager.get_result()

        foodDataManager.get_anteatery_food('lunch')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.ant_lunch = foodDataManager.get_result()

        foodDataManager.get_anteatery_food('dinner')
        foodDataManager.process_available_data()
        foodDataManager.process_result()
        self.ant_dinner = foodDataManager.get_result()

        self.__classDataManager = ClassDataManager()

    def __fetch_class_data(self):
        for i in range(len(self.__entry_vars)):
            self.__classDataManager.update_data(self.__entry_fields[i], self.__entry_vars[i].get())

        self.__classDataManager.set_html_target()
        self.__classDataManager.process_available_data()
        self.__classDataManager.process_result()

        self.__classData = self.__classDataManager.get_result()

    def redraw(self):
        self.draw_content(None)
        self.draw_menu(None)
        self.draw_title(None)

    def go_to_tab(self, target_index):
        self.__current_button = target_index
        self.redraw()

    def clear_canvas(self, canvas):
        canvas.delete(tk.ALL)

    def fetch_new_map(self, classroom = None):
        if classroom == 'ELH 100':
            self.__current_icon = 12
        elif classroom == 'HH 178':
            self.__current_icon = 11
        elif classroom == 'HSLH 100A':
            self.__current_icon = 13
        elif classroom == 'ICS 174':
            self.__current_icon = 14
        else:
            self.__current_icon = 10

    #
    # CANVAS DRAWING
    #

    def draw_title(self, event):
        self.clear_canvas(self.__title_canvas)

        canvas_width = self.__nav_canvas.winfo_width()
        canvas_height = self.__nav_canvas.winfo_height()

        self.__title_canvas.create_rectangle(0, 0, canvas_width, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        title = ""
        subtitle = ""

        if self.__current_button == 1:
            title = "MAPS"
            if(self.__current_icon == 10):
                subtitle = "No Route"
            else:
                subtitle = "Route to " + ["HH 178", "ELH 100", "HSLH 100A", "ICS 174"][self.__current_icon-11]
        elif self.__current_button == 2:
            title = "FOOD"
            subtitle = ["PIPPINS", "BRANDYWINE", "THE ANTEATERY"][self.__FOOD_COUNT]
        elif self.__current_button == 3:
            title = date.today().strftime("%A, %B %d %Y")
            subtitle = self.__days[self.__DAY_COUNT]
        elif self.__current_button == 4:
            title = "WEB REG"
            subtitle = "LISTING"
        elif self.__current_button == 5:
            title = "EVENTS"
            subtitle = "LISTING"

        self.draw_textblock(self.__title_canvas, title, 0, 0, canvas_width, self.__DIMMENSIONS["banner"][1], font_size=16, modifier="bold", center=True, bg_color=self.__PRIMARY_COLOR, text_color=self.__SECONDARY_COLOR)

        self.draw_textblock(self.__title_canvas, subtitle, 0, self.__DIMMENSIONS["banner"][1], canvas_width, self.__DIMMENSIONS["banner"][1], font_size=16, modifier="bold", center=True)

    def draw_menu(self, event):
        self.clear_canvas(self.__nav_canvas)
        self.__buttons = []
        self.__button_images = []

        canvas_width = self.__nav_canvas.winfo_width()
        canvas_height = self.__nav_canvas.winfo_height()

        for i in range(5):
            x0 = i * self.__DIMMENSIONS["navigation"][0]
            y0 = 0

            if i+1 == self.__current_button:
                self.__buttons.append(self.__nav_canvas.create_image(x0 - 39 + self.__DIMMENSIONS["navigation"][0], y0 - 39 + self.__DIMMENSIONS["navigation"][1], image=self.__icons[i+5]))
            else:
                self.__buttons.append(self.__nav_canvas.create_image(x0 - 39 + self.__DIMMENSIONS["navigation"][0], y0 - 39 + self.__DIMMENSIONS["navigation"][1], image=self.__icons[i]))

    def draw_content(self, event):
        self.clear_canvas(self.__content_canvas)
        self.__course_buttons = []

        if self.__current_button == 1:
            self.__draw_maps()
        elif self.__current_button == 2:
            self.__draw_food()
        elif self.__current_button == 3:
            self.__draw_planner()
        elif self.__current_button == 4:
            self.__draw_webReg()
        elif self.__current_button == 5:
            self.__draw_events()

    #
    # DRAWING UTILITY
    #
    def draw_textblock(self, canvas, in_text, x0, y0, max_width, max_height, bg_color = None, text_color = None, font_size = 12, scrollable = False, padding = 10, modifier=None, center=False):
        if(bg_color == None):
            bg_color = self.__SECONDARY_COLOR

        if(text_color == None):
            text_color = self.__PRIMARY_COLOR

        boundingBox = ""

        if(scrollable):
            boundingBox = canvas.create_rectangle(x0, y0, x0 + max_width, y0 + max_height, fill=bg_color, tags="scrollable")
            if(center):
                canvas.create_text(x0 + max_width/2, y0 + max_height/2, fill=text_color, tags="scrollable", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
            else:
                canvas.create_text(x0 + padding, y0 + padding, fill=text_color, anchor="nw", tags="scrollable", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
        else:
            boundingBox = canvas.create_rectangle(x0, y0, x0 + max_width, y0 + max_height, fill=bg_color)
            if(center):
                canvas.create_text(x0 + max_width/2, y0 + max_height/2, fill=text_color, width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
            else:
                canvas.create_text(x0 + padding, y0 + padding, fill=text_color, anchor="nw", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))

        return boundingBox

    #
    # DRAWING MACROS
    #
    def __draw_maps(self):
        canvas_width = self.__content_canvas.winfo_width()
        canvas_height = self.__content_canvas.winfo_height()

        self.__content_canvas.create_image(canvas_width/2, canvas_height/2, image=self.__icons[self.__current_icon])

    def __draw_food(self):
        food_dict = {}
        if(self.__FOOD_COUNT == 0):
            if(self.__FOOD_PERIOD == 0):
                food_dict = self.pip_breakfast
            elif(self.__FOOD_PERIOD == 1):
                food_dict = self.pip_lunch
            elif(self.__FOOD_PERIOD == 2):
                food_dict = self.pip_dinner

        elif(self.__FOOD_COUNT == 1):
            if(self.__FOOD_PERIOD == 0):
                food_dict = self.brand_lunch
            elif(self.__FOOD_PERIOD == 1):
                food_dict = self.brand_lunch
            elif(self.__FOOD_PERIOD == 2):
                food_dict = self.brand_dinner
        elif(self.__FOOD_COUNT == 2):
            if(self.__FOOD_PERIOD == 0):
                food_dict = self.ant_breakfast
            elif(self.__FOOD_PERIOD == 1):
                food_dict = self.ant_lunch
            elif(self.__FOOD_PERIOD == 2):
                food_dict = self.ant_dinner

        for i, food in enumerate(food_dict.keys()):
            string = food + "\n" + food_dict[food]

            self.draw_textblock(self.__content_canvas, string, 0, i * self.__DIMMENSIONS["food"][1] + i* self.__tile_margins, self.__DIMMENSIONS["food"][0], self.__DIMMENSIONS["food"][1], scrollable=True)

        self.__content_canvas.tag_lower("scrollable")

    def __draw_planner(self):
        if(self.__DAY_COUNT in [0, 2, 4]):
            for i, course in enumerate(self.__classes):
                self.__course_buttons.append(self.draw_textblock(self.__content_canvas, course, 0, i * self.__DIMMENSIONS["class"][1] + i* self.__tile_margins, self.__DIMMENSIONS["class"][0], self.__DIMMENSIONS["class"][1], scrollable=True))

    def __draw_webReg(self):
        counter = 0
        for var in self.__entry_vars:
            self.draw_textblock(self.__content_canvas, self.__entry_fields[counter], 0, counter * self.__DIMMENSIONS["event"][1] + counter*self.__tile_margins, self.__DIMMENSIONS["event"][0], self.__DIMMENSIONS["event"][1], scrollable=True)

            e = tk.Entry(self.__content_canvas, textvariable=var, width=25)

            self.__content_canvas.create_window(self.__content_canvas.winfo_width()*7/10, (counter + .5) * self.__DIMMENSIONS["event"][1] + counter*self.__tile_margins, window = e)

            self.__content_canvas.update()

            counter += 1

        self.__submit_button = self.draw_textblock(self.__content_canvas, "Update Search!", 0, counter * self.__DIMMENSIONS["event"][1] + counter*self.__tile_margins, self.__DIMMENSIONS["event"][0], self.__DIMMENSIONS["event"][1], center = True, scrollable=True)
        counter += 1

        if(self.__classData != None):
            for course in self.__classData:
                self.draw_textblock(self.__content_canvas, course, 0, counter * self.__DIMMENSIONS["event"][1] + counter*self.__tile_margins, self.__DIMMENSIONS["event"][0], self.__DIMMENSIONS["event"][1], center = True, scrollable=True)
                counter += 1


    def __draw_events(self):
        for i, string in enumerate(self.__events):
            self.draw_textblock(self.__content_canvas, string, 0, i * self.__DIMMENSIONS["event"][1] + i* self.__tile_margins, self.__DIMMENSIONS["event"][0], self.__DIMMENSIONS["event"][1], scrollable=True)

    #
    # EVENT HANDLERS
    #
    def __content_click(self, event):
        self.__set_origin(event)

        if(self.__current_button in [3, 4]):
            closest = event.widget.find_overlapping(event.x, event.y, event.x+1, event.y+1)
            under = event.widget.find_below(closest)
            if(len(closest) == 0):
                return
            elif(len(under) == 0):
                under = closest # lazy af

            if(self.__current_button == 3):
                for i, course in enumerate(self.__course_buttons):
                    if(course in [closest[0], under[0]]):
                        self.fetch_new_map(self.__classes[i].split("@ ")[-1])
                        self.go_to_tab(1)
            elif(self.__current_button == 4):
                if(self.__submit_button in [closest[0], under[0]]):
                    self.__fetch_class_data()
                    self.redraw()

    def __set_origin(self, event):
        self.__xorigin, self.__yorigin = event.x, event.y

    def handle_radio(self, event):
        button_num = (event.x // self.__DIMMENSIONS["navigation"][0]) + 1
        debug_print("Clicked at ({0},{1}) => # {2})".format(event.x, event.y, button_num))

        if(button_num == self.__current_button):
            if(button_num == 1):
                self.fetch_new_map()
            elif(button_num == 2):
                self.__FOOD_COUNT += 1
                if(self.__FOOD_COUNT >= 3):
                    self.__FOOD_COUNT = 0
            elif(button_num == 3):
                self.__DAY_COUNT += 1
                if(self.__DAY_COUNT >= len(self.__days)):
                    self.__DAY_COUNT = 0
        else:
            if(button_num == 1):
                self.fetch_new_map()
            self.__current_button = button_num

        self.redraw()

    def __scroll_scrollables(self, event):
        if self.__yorigin != event.y:
            self.__content_canvas.move("scrollable", 0, event.y - self.yscroll_last)
        self.yscroll_last = event.y

    def __set_scroll_last(self, event):
        self.yscroll_last = event.y

if __name__ == '__main__':
    print("FILE TESTING")
    win = GUI()
    win.run()
    print("TEST CLONCLUDED")
    exit()
