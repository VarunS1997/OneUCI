from tkinter import *
from datetime import date

class GUI:

    def __init__(self):
        
        self.event_list_counter = 0
        self.events = []
        self.gui = Tk()

        self.canvas = Canvas(self.gui, width=400, height=640)

        self.b1 = self.canvas.create_rectangle(0, 560, 80, 640, fill="#1B3D6D", tags="Planner")
        self.b2 = self.canvas.create_rectangle(80, 560, 160, 640, fill="#1B3D6D", tags="Food")
        self.b3 = self.canvas.create_rectangle(160, 560, 240, 640, fill="#1B3D6D", tags="Maps")
        self.b4 = self.canvas.create_rectangle(240, 560, 320, 640, fill="#1B3D6D", tags="WebReg")
        self.b5 = self.canvas.create_rectangle(320, 560, 400, 640, fill="#1B3D6D", tags="Events")
        
    def Radio_Button(self, event):
        print("clicked at", event.x, event.y)
        for x in [self.canvas.find_withtag("Planner")[0],
                  self.canvas.find_withtag("Food")[0],
                  self.canvas.find_withtag("Maps")[0],
                  self.canvas.find_withtag("WebReg")[0],
                  self.canvas.find_withtag("Events")[0]]:
            if event.widget.find_closest(event.x, event.y)[0] == x:
                self.canvas.itemconfig(event.widget.find_closest(event.x, event.y)[0], fill="#FFD200")
            else:
                self.canvas.itemconfig(x, fill="#1B3D6D")
                
        if self.canvas.find_withtag("Planner")[0] == event.widget.find_closest(event.x, event.y)[0]:
            self.draw_Planner()
        elif self.canvas.find_withtag("Food")[0] == event.widget.find_closest(event.x, event.y)[0]:
            self.draw_Food()
        elif self.canvas.find_withtag("Maps")[0] == event.widget.find_closest(event.x, event.y)[0]:
            self.draw_Maps()
        elif self.canvas.find_withtag("WebReg")[0] == event.widget.find_closest(event.x, event.y)[0]:
            self.draw_WebReg()
        elif self.canvas.find_withtag("Events")[0] == event.widget.find_closest(event.x, event.y)[0]:
            self.draw_Events()

    def redraw_buttons_Planner(self):
        overlap = self.canvas.find_overlapping(1, 639, 399, 639)
        for x in overlap:
            self.canvas.delete(x)
        
        self.b1 = self.canvas.create_rectangle(0, 560, 80, 640, fill="#FFD200", tags="Planner")
        self.b2 = self.canvas.create_rectangle(80, 560, 160, 640, fill="#1B3D6D", tags="Food")
        self.b3 = self.canvas.create_rectangle(160, 560, 240, 640, fill="#1B3D6D", tags="Maps")
        self.b4 = self.canvas.create_rectangle(240, 560, 320, 640, fill="#1B3D6D", tags="WebReg")
        self.b5 = self.canvas.create_rectangle(320, 560, 400, 640, fill="#1B3D6D", tags="Events")
    
    def clear_view(self):
        overlap = self.canvas.find_overlapping(5, 5, 315, 555)
        for x in overlap:
            self.canvas.delete(x)
            
    def draw_block(self, time1, time2, place) -> None:
        '''create a block for the specified fields and have the blocks scrollable.'''
        self.canvas.create_rectangle()

    def scroll_block(self):
        for block in self.events:
            self.draw_block(block.time1, block.time2, block.place)
        
        
    def remove_block(self, block_tup):
        self.events.pop(block_tup)
    
    def draw_Planner(self):
        self.clear_view()
        self.canvas.create_rectangle(0, 0, 400, 40, fill="#1B3D6D")
        self.canvas.create_text(200, 20, fill="white", font="Helvetica 20 bold italic", text=date.today().strftime("%A, %B %d %Y"))

    def draw_Food(self):
        self.clear_view()

    def draw_Maps(self):
        self.clear_view()

    def draw_WebReg(self):
        self.clear_view()

    def draw_Events(self):
        self.clear_view()
        
    def pack(self):
        
        self.canvas.tag_bind("Planner", '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind("Food", '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind("Maps", '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind("WebReg", '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind("Events", '<ButtonPress-1>', self.Radio_Button)

        self.canvas.pack()
        self.gui.mainloop()


guis = GUI()    
guis.pack()

