import tkinter as tk
#from debugging import *
from datetime import date

def get_dimmensions():
    dimmensions = {}
    dimmensions["navigation"] = (80, 80)
    dimmensions["banner"] = (400, 40)
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
                tk.PhotoImage(file='icons/uci_events_selected.gif')]

        self.__content_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DISPLAY_HEIGHT-self.__DIMMENSIONS["navigation"][1])
        self.__content_canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__content_canvas.bind('<Button-1>', self.__set_origin)
        self.__content_canvas.bind('<B1-Motion>', self.__scroll_scrollables)
        self.__content_canvas.bind('<Motion>', self.__set_scroll_last)
        self.__content_canvas.bind('<Configure>', self.draw_content)

        self.__nav_canvas = tk.Canvas(master = self.__top, width=self.__DISPLAY_WIDTH, height=self.__DIMMENSIONS["navigation"][1], cursor='hand2')
        self.__nav_canvas.grid(row = 1, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.__nav_canvas.bind('<Button-1>', self.handle_radio)
        self.__nav_canvas.bind('<Configure>', self.draw_menu)

    def run(self):
        self.__top.mainloop()

    def redraw(self):
        self.draw_menu(None)
        self.draw_content(None)

    def clear_canvas(self, canvas):
        canvas.delete(tk.ALL)

    def handle_radio(self, event):
        button_num = (event.x // self.__DIMMENSIONS["navigation"][0]) + 1
        #debug_print("Clicked at ({0},{1}) => # {2})".format(event.x, event.y, button_num))
        self.__current_button = button_num
        self.redraw()

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

    def draw_block(self, time1, time2,  place):
        #check for space to draw the box
        ycoord = 50 + (self.block_counter * 50)
        block = self.__content_canvas.create_rectangle(0, ycoord, 400, ycoord + 30, fill="red", tags="scrollable")
        text = self.__content_canvas.create_text(200, ycoord + 20, text=time1 + "-" + time2 + " : " + place, tags="scrollable")
        self.block_counter += 1

    def __set_origin(self, event):
        self.__xorigin, self.__yorigin = event.x, event.y

    def __draw_planner(self):
        self.__content_canvas.create_rectangle(0, 0, self.__DISPLAY_WIDTH, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        self.__content_canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text=date.today().strftime("%A, %B %d %Y"))

        self.block_counter = 0
        #example boxes
        self.draw_block("5:00", "6:00", "DBH")
        self.draw_block("7:00", "7:50", "MSTB")
        self.draw_block("9:00", "9:50", "SC2")
        
        self.__content_canvas.tag_lower("scrollable")

    def __scroll_scrollables(self, event):
        if self.__yorigin != event.y:
            self.__content_canvas.move("scrollable", 0, event.y - self.yscroll_last)
        self.yscroll_last = event.y
        
    def __set_scroll_last(self, event):
        self.yscroll_last = event.y

    def __draw_food(self):
        self.__content_canvas.create_rectangle(0, 0, self.__DISPLAY_WIDTH, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        self.__content_canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text="FOOD")

    def __draw_maps(self):
        self.__content_canvas.create_rectangle(0, 0, self.__DISPLAY_WIDTH, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        self.__content_canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text="MAPS")

    def __draw_webReg(self):
        self.__content_canvas.create_rectangle(0, 0, self.__DISPLAY_WIDTH, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        self.__content_canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text="WEBREG")

    def __draw_events(self):
        self.__content_canvas.create_rectangle(0, 0, self.__DISPLAY_WIDTH, self.__DIMMENSIONS["banner"][1], fill=self.__PRIMARY_COLOR)

        self.__content_canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text="EVENTS")

if __name__ == '__main__':
    print("FILE TESTING")
    win = GUI()
    win.run()
    print("TEST CLONCLUDED")
    exit()
