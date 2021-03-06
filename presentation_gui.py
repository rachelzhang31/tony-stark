import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import pyautogui

WIDTH = 1000
HEIGHT = 800

class PresentationAPP(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, x, y):
        # the root will be self
        tk.Tk.__init__(self)
        self.geometry('+100+100')
        
        self.MOUSE_X, self.MOUSE_Y = pyautogui.position()

        # CHANGE THESE SOURCE FILES TO SLIDESHOW LOOKING IMAGES
        self.picture_sources = [
            "Backgrounds\\Slide1.PNG",
            "Backgrounds\\Slide2.PNG",
            "Backgrounds\\Slide3.PNG",
            "Backgrounds\\Slide4.PNG"
        ]
        self.pictures = []
        self.slide_index = 0
        self.title("Powerpoint Emulation")
   
        # BUTTONS
        self.font = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.previous_slide = tk.Button(self, text='Previous Slide', width=30, command= lambda: self.show_slides("BACKWARD"), font=self.font, cursor="dotbox")
        self.previous_slide.grid(column=1, row = 1)

        #self.exit_button = tk.Button(self, text='Exit', width=30, command=self.destroy, font=self.font, cursor="dotbox")
        #self.exit_button.grid(column=2, row = 1)

        self.next_slide = tk.Button(self, text='Next Slide', width=30, command= lambda: self.show_slides("FORWARD"), font=self.font, cursor="dotbox")
        self.next_slide.grid(column=3, row = 1)

        self.picture_display = tk.Label(self, cursor="circle")
        self.picture_display.grid(column=1, row = 2, columnspan = 3)


    def show_slides(self, direction):
        offset = 1 if direction == "FORWARD" else -1        
        self.slide_index = (self.slide_index + offset) % len(self.picture_sources)

        self.picture_display.img = self.pictures[self.slide_index] # reference so it isn't deleted
        self.picture_display.config(image=self.pictures[self.slide_index])

    def init_images(self):
        for image_src in self.picture_sources:
            self.pictures.append(
                ImageTk.PhotoImage(
                    Image.open(image_src).resize((WIDTH, HEIGHT), Image.ANTIALIAS)
                )
            )

    def click(self):
        pyautogui.click(self.MOUSE_X, self.MOUSE_Y)

    def move_mouse(self, x_offset, y_offset):
        self.MOUSE_X += x_offset
        self.MOUSE_Y += y_offset
        pyautogui.moveTo(self.MOUSE_X, self.MOUSE_Y)

    
    def queue_event(self, q):
        try:
            event = q.get(timeout=0.01)
            
            # TILT-FORWARD
            if event[0] == 0:
                self.show_slides("FORWARD")
            # TILT-BACKWARDS
            elif event[0] == 1:
                self.show_slides("BACKWARDS")
            # CLICK EVENT
            elif event[0] == 2:
                self.click()
            # MOUSE MOVE EVENT, ADD X Y as other args
            elif event[0] == 3:
                self.move_mouse(event[1], event[2])
            else:
                print("Unkown event argument)")
        except:
            pass

        self.after(10, lambda: self.queue_event(q))


    def run(self, q):
        self.after(500, lambda: self.queue_event(q))
        self.mainloop()

# app = PresentationAPP(WIDTH, HEIGHT)
# app.init_images()
# app.show_slides("FORWARD")
# app.run()
