from tkinter import *
from datetime import date
from VerticalScrollFrame import *


class GUI:
    def __init__(self):
        
        self.gui = Tk()
        
        

        self.canvas = Canvas(self.gui, width=400, height=640)

        self.b1 = self.canvas.create_rectangle(0, 560, 80, 640, fill="#1B3D6D")
        self.b2 = self.canvas.create_rectangle(80, 560, 160, 640, fill="#1B3D6D")
        self.b3 = self.canvas.create_rectangle(160, 560, 240, 640, fill="#1B3D6D")
        self.b4 = self.canvas.create_rectangle(240, 560, 320, 640, fill="#1B3D6D")
        self.b5 = self.canvas.create_rectangle(320, 560, 400, 640, fill="#1B3D6D")
        
    def Radio_Button(self, event):
        print("clicked at", event.x, event.y)
        for x in range(1,6):
            if event.widget.find_closest(event.x, event.y)[0] == x:
                self.canvas.itemconfig(event.widget.find_closest(event.x, event.y)[0], fill="#FFD200")
            else:
                self.canvas.itemconfig(x, fill="#1B3D6D")
                
        if event.widget.find_closest(event.x, event.y)[0] == 1:
            self.draw_Planner()
        elif event.widget.find_closest(event.x, event.y)[0] == 2:
            self.draw_Food()
        elif event.widget.find_closest(event.x, event.y)[0] == 3:
            self.draw_Maps()
        elif event.widget.find_closest(event.x, event.y)[0] == 4:
            self.draw_WebReg()
        elif event.widget.find_closest(event.x, event.y)[0] == 5:
            self.draw_Events()
            
    def clear_view(self):
        overlap = self.canvas.find_overlapping(5, 5, 315, 555)
        print(overlap)
        for x in overlap:
            self.canvas.delete(x)
            
    def draw_block(self, time1, time2,  place):
        pass
    
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
        
        self.canvas.tag_bind(self.b1, '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind(self.b2, '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind(self.b3, '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind(self.b4, '<ButtonPress-1>', self.Radio_Button)
        self.canvas.tag_bind(self.b5, '<ButtonPress-1>', self.Radio_Button)
        
        self.canvas.pack()
        self.gui.mainloop()


guis = GUI()    
guis.pack()

