import tkinter as tk
from UDA_debugging import *
from datetime import date

def get_dimmensions():
    dimmensions = {}
    dimmensions["navigation"] = (80, 80)
    dimmensions["banner"] = (400, 40)
    dimmensions["food"] = (400, 120)
    dimmensions["class"] = (400, 60)
    return dimmensions

class GUI:
    def __init__(self, DISPLAY_WIDTH = 400, DISPLAY_HEIGHT = 640, PRIMARY_COLOR = "#00255D", SECONDARY_COLOR = "#FFD200"):
        self.__PRIMARY_COLOR = PRIMARY_COLOR
        self.__SECONDARY_COLOR = SECONDARY_COLOR

        self.__DISPLAY_WIDTH = DISPLAY_WIDTH
        self.__DISPLAY_HEIGHT = DISPLAY_HEIGHT

        self.__DIMMENSIONS = get_dimmensions()

        self.__buttons = []
        self.__button_images = []
        self.__current_button = 3
        self.__xorigin = 0
        self.__yorigin = 0
        self.__tile_margins = 10
        self.__FOOD_COUNT = 0
        self.__DAY_COUNT = 0


        self.__top = tk.Tk()

        self.icons = [tk.PhotoImage(file='icons/uci_maps.gif'),
                tk.PhotoImage(file='icons/uci_food.gif'),
                tk.PhotoImage(file='icons/uci_planner.gif'),
                tk.PhotoImage(file='icons/uci_webreg.gif'),
                tk.PhotoImage(file='icons/uci_events.gif'),
                tk.PhotoImage(file='icons/uci_maps_selected.gif'),
                tk.PhotoImage(file='icons/uci_food_selected.gif'),
                tk.PhotoImage(file='icons/uci_planner_selected.gif'),
                tk.PhotoImage(file='icons/uci_webreg_selected.gif'),
                tk.PhotoImage(file='icons/uci_events_selected.gif'),
                tk.PhotoImage(file='icons/map_img.gif')]

        self.__title_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DIMMENSIONS["banner"][1]*2)
        self.__title_canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__title_canvas.bind('<Configure>', self.draw_title)

        self.__content_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DISPLAY_HEIGHT-self.__DIMMENSIONS["banner"][1]*2-self.__DIMMENSIONS["navigation"][1])
        self.__content_canvas.grid(row = 1, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__content_canvas.bind('<Button-1>', self.__set_origin)
        self.__content_canvas.bind('<B1-Motion>', self.__scroll_scrollables)
        self.__content_canvas.bind('<Motion>', self.__set_scroll_last)
        self.__content_canvas.bind('<Configure>', self.draw_content)

        self.__nav_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DIMMENSIONS["navigation"][1], cursor='hand2')
        self.__nav_canvas.grid(row = 2, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__nav_canvas.bind('<Button-1>', self.handle_radio)
        self.__nav_canvas.bind('<Configure>', self.draw_menu)

        self.pip = {}
        self.brand = {}
        self.ant = {}

        self.days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']

    def run(self):
        self.__top.mainloop()

    def redraw(self):
        self.draw_content(None)
        self.draw_menu(None)
        self.draw_title(None)

    def clear_canvas(self, canvas):
        canvas.delete(tk.ALL)

    def retrieve_food(self, pip, brand, ant):
        self.pip = pip
        self.brand = brand
        self.ant = ant

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
            subtitle = "No Route"
        elif self.__current_button == 2:
            title = "FOOD"
            subtitle = ["PIPPINS", "BRANDYWINE", "THE ANTEATERY"][self.__FOOD_COUNT]
        elif self.__current_button == 3:
            title = date.today().strftime("%A, %B %d %Y")
            subtitle = self.days[self.__DAY_COUNT]
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
                self.__buttons.append(self.__nav_canvas.create_image(x0 - 39 + self.__DIMMENSIONS["navigation"][0], y0 - 39 + self.__DIMMENSIONS["navigation"][1], image=self.icons[i+5]))
            else:
                self.__buttons.append(self.__nav_canvas.create_image(x0 - 39 + self.__DIMMENSIONS["navigation"][0], y0 - 39 + self.__DIMMENSIONS["navigation"][1], image=self.icons[i]))

    def draw_content(self, event):
        self.clear_canvas(self.__content_canvas)

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

        if(scrollable):
            canvas.create_rectangle(x0, y0, x0 + max_width, y0 + max_height, fill=bg_color, tags="scrollable")
            if(center):
                canvas.create_text(x0 + max_width/2, y0 + max_height/2, fill=text_color, tags="scrollable", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
            else:
                canvas.create_text(x0 + padding, y0 + padding, fill=text_color, anchor="nw", tags="scrollable", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
        else:
            canvas.create_rectangle(x0, y0, x0 + max_width, y0 + max_height, fill=bg_color)
            if(center):
                canvas.create_text(x0 + max_width/2, y0 + max_height/2, fill=text_color, width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))
            else:
                canvas.create_text(x0 + padding, y0 + padding, fill=text_color, anchor="nw", width=max_width, text=in_text, font="Courier " + str(font_size) + " " + str(modifier or ""))

    def draw_block(self, class_name, time1, time2,  place):
        #check for space to draw the box
        ycoord = 100 + (self.block_counter * 50)
        #block = self.__content_canvas.create_rectangle(0, ycoord, 400, ycoord + 30, fill="red", tags="scrollable")
        text = self.__content_canvas.create_text(200, ycoord + 20,fill="blue", font='Courier 16 bold', text=class_name + ': ' + time1 + "-" + time2 + " @ " + place, tags="scrollable")

        self.block_counter += 1

    #
    # DRAWING MACROS
    #
    def __draw_maps(self):
        self.__content_canvas.create_image(200, 300, image=self.icons[10])

    def __draw_food(self):
        food_dict = {}
        if(self.__FOOD_COUNT == 0):
            food_dict = self.pip
        elif(self.__FOOD_COUNT == 1):
            food_dict = self.brand
        elif(self.__FOOD_COUNT == 2):
            food_dict = self.ant

        for i, food in enumerate(food_dict.keys()):
            string = food + "\n" + food_dict[food]

            self.draw_textblock(self.__content_canvas, string, 0, i * self.__DIMMENSIONS["food"][1] + i* self.__tile_margins, self.__DIMMENSIONS["food"][0], self.__DIMMENSIONS["food"][1], scrollable=True)
            
        self.__content_canvas.tag_lower("scrollable")

    def __draw_planner(self):
        if(self.__DAY_COUNT == 1 or self.__DAY_COUNT == 3):
            classes = ["CS 122B: 11:00-12:20 @ HSLH 100A", "CS 162: 12:30-1:50 @ ICS 174", "GEN&SEX 40B: 2:00-3:20 @ ELH 100", "CS 167: 3:30-4:50 @ HH 178"]
            for i, string in enumerate(classes):
                self.draw_textblock(self.__content_canvas, string, 0, i * self.__DIMMENSIONS["class"][1] + i* self.__tile_margins, self.__DIMMENSIONS["class"][0], self.__DIMMENSIONS["class"][1], scrollable=True)

    def __draw_webReg(self):
        self.__content_canvas.create_text(200, 200, fill='blue', font="Courier 20 bold", text="HACK UCI ALL DAY EVERY DAY")

        self.__content_canvas.create_text(200, 240, fill='blue', font="Courier 20 bold", text="122B PROJECT 1 DUE WED 11:55PM")

    def __draw_events(self):
        self.__content_canvas.create_text(200, 200, fill='blue', font="Courier 20 bold", text="HACK UCI ALL DAY EVERY DAY")

        self.__content_canvas.create_text(200, 240, fill='blue', font="Courier 20 bold", text="122B PROJECT 1 DUE WED 11:55PM")


    # EVENT HANDLERS

    def __set_origin(self, event):
        self.__xorigin, self.__yorigin = event.x, event.y

    def handle_radio(self, event):
        button_num = (event.x // self.__DIMMENSIONS["navigation"][0]) + 1
        debug_print("Clicked at ({0},{1}) => # {2})".format(event.x, event.y, button_num))

        if(button_num == self.__current_button):
            if(button_num == 2):
                self.__FOOD_COUNT += 1
            elif(button_num == 3):
                self.__DAY_COUNT += 1
        else:
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
