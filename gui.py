#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:00:00 2020

@author: dlppdl
"""

#Importing necessary modules
from tkinter import Tk,Label,Button,Frame,LEFT,RIGHT,TOP,BOTTOM,Canvas,PhotoImage,Menu,NW
from PIL import ImageTk,Image
import cv2
import numpy as np
import re
import os
from itertools import count
from detector import Detector

#Parent window title, icon, size
root=Tk() 
root.title("")
root.call('wm', 'iconphoto', root._w, PhotoImage(file='./icon/icon.png'))
root.geometry("480x590")

#Key 'Escape' destroy the window
root.bind('<Escape>', lambda e: root.destroy())

#Disabling the resizable cababilty horizontally and vertically
root.resizable(False,False)

dl = Detector()

#Title class is where the title of GUI and homepage button goes
class Title:    
    def __new__(cls):

        cls.title_frame = Frame(root, bd = 0 , relief = "raise")
        cls.title_frame.pack(side = TOP)
        
        cls.home_icon = Icon( "icon/home.png")
        cls.home_button = Button(cls.title_frame, image = cls.home_icon,
                                 command = Home, width = 70, height = 50,bd = 0)
        cls.home_button.pack(side = LEFT)
        HoverText(cls.home_button, "Home")
        
        cls.title = Image.open("icon/title.png")
        cls.title = ImageTk.PhotoImage(cls.title)
        cls.title_label = Label(cls.title_frame, image = cls.title)
        cls.title_label.image = cls.title 
        cls.title_label.pack(side = RIGHT)

#Class Icon resize the given icon file and return the resized photo
class Icon:
    def __new__(cls, file):
        cls.icon = PhotoImage(file = file)   
        cls.icon = cls.icon.subsample(3,3)
        return cls.icon

#This class gets all the frames of GIF one by one and show them continuously looks like GIF play
class PlayGIF(Label):
    def load(self, gif):
        if isinstance(gif, str):
            gif = Image.open(gif)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(i)
        except EOFError:
            pass

        try:
            self.delay = gif.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

#The frontal page of GUI with GIF, title, and buttons
class Home:
    def __new__(cls):
        global filter_code
        
        destroy()
        Title()
        
        filter_code = 0
        
        lbl = PlayGIF(root)
        lbl.pack()
        lbl.load('icon/gif.gif')
        lbl.config(bd = 0)
        
        cls.camera_icon = Icon( "icon/camera.png")
        camera_button = Button(root, image = cls.camera_icon,command = Camera,
                               width = 70, height = 50,bd = 0)
        camera_button.pack(side = BOTTOM)
        HoverText(camera_button, "Open Camera")

#When you hover over any buttons the text shown in screen the basic works of that thing goes here
class HoverText(Menu):
    def __init__(self, parent, text, command=None):
       Menu.__init__(self,parent, tearoff=0)

       text = re.split('\n', text)
       
       for t in text:
          self.add_command(label = t)
       
       self._displayed=False
       self.master.bind("<Enter>",self.display )
       self.master.bind("<Leave>",self.remove )

    def display(self,event):
       if not self._displayed:
          self._displayed=True
          self.post(event.x_root+1, event.y_root+1)

    def remove(self, event):
     if self._displayed:
       self._displayed=False
       self.unpost()

#It destroys if anything running on the parent window
def destroy():
    for window in root.winfo_children():
        window.destroy()

    try:
        cam.release()
    except:
        pass

#Selection of filter and applying them
class Filter:
    def __init__(self):
        self.button()

    def glass(self):
        global filter_code

        filter_code = 1
        
    def face_mask(self):
        global filter_code

        filter_code = 2  

    def hat(self):
        global filter_code
        
        filter_code = 3
        
    def thug(self):
        global filter_code

        filter_code = 4

    def mustache(self):
        global filter_code

        filter_code = 5
                   
    def button(self):        
        frame = Frame(root,width = 480,height = 50, bd = 0)
        frame.pack(side = BOTTOM)
        
        width = 80
        height = 60
        
        self.glass_icon = Icon( "icon/glass.png")
        glass_button = Button(frame, image = self.glass_icon,command = self.glass,
               			width = width, height = height, bd = 0)
        glass_button.grid(row= 0, column = 0)
        
        self.face_mask_icon = Icon("icon/face_mask.png")
        face_mask_button = Button(frame, image = self.face_mask_icon, command = self.face_mask,
                             width = width, height = height, bd = 0)
        face_mask_button.grid(row = 0, column =1)
        
        self.hat_icon = Icon( "icon/hat.png")
        hat_button = Button(frame, image = self.hat_icon,command = self.hat,
                               width = width, height = height, bd = 0)      
        hat_button.grid(row = 0, column = 2)
        
        self.thug_icon = Icon("icon/thug_icon.png")
        thug_button = Button(frame, image = self.thug_icon, command = self.thug,
                             width = width, height = height, bd = 0)
        thug_button.grid(row = 0, column = 3)

        self.mustache_icon = Icon("icon/mustache.png")
        mustache_button = Button(frame, image = self.mustache_icon, command = self.mustache,
                             width = width, height = height, bd = 0)
        mustache_button.grid(row = 0, column =4)
        
#Camera access displaying video with or without filter
class Camera:
    
    def __new__(cls):
        global cam,last_frame
        
        destroy()
        Title()
        
        last_frame = np.zeros((480, 480, 3), dtype=np.uint8)
        cam = cv2.VideoCapture(0)
        
        def video():     
            if not cam.isOpened():
                print("cant open the camera")
                
            flag, frame = cam.read()
            frame_flip = cv2.flip(frame, 1)
            frame = frame_flip[0:480,80:560]
            
            if flag is None:
                print ("Major error!")
            elif flag:
                last_frame = frame.copy()
            
            land = dl.detect_landmark(last_frame,filter_code)
            
            color_correction = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)     
            array_image = Image.fromarray(color_correction)
            photo = ImageTk.PhotoImage(image=array_image)
            
            canvas.photo = photo
            canvas.create_image(0,0,image=photo,anchor = NW)
            
            try:
                if filter_code == 1:

                    img = Image.open('icon/glass.png')
                    new_width  = int(land[16][0] - land[0][0])
                    new_height = int(land[30][1] - (land[21][1]+land[22][1])/2)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img.save('icon/glass_r.png')

                    glass = PhotoImage(file = 'icon/glass_r.png')
                    os.remove('icon/glass_r.png')
                    canvas.create_image((land[21][0]+land[22][0])/2,land[27][1]+8, image = glass)
                    canvas.glass = glass
                                
                elif filter_code == 2:

                    img = Image.open('icon/face_mask.png')
                    new_width  = int(land[15][0] - land[1][0]) + 6
                    new_height = int(land[9][1] - land[29][1] + 12)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img.save('icon/face_mask_r.png')

                    glass3 = PhotoImage(file = 'icon/face_mask_r.png')
                    canvas.create_image((land[3][0]+land[13][0])/2,int((land[9][1] + land[29][1] + 12)/2), image = glass3)
                    canvas.glass3 = glass3
                    
                elif filter_code == 3:
                    img = Image.open('icon/hat.png')
                    new_width  = int(land[16][0] - land[0][0])
                    new_height = img.size[1] + 20
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img.save('icon/hat_r.png')

                    hat = PhotoImage(file = 'icon/hat_r.png')
                    canvas.create_image((land[16][0]+land[0][0])/2,land[27][1]-150, image = hat)
                    canvas.hat = hat
                                   
                elif filter_code == 4:
                    img = Image.open('icon/thug.png')
                    new_width  = int(land[16][0] - land[0][0]) - 5
                    new_height = int(land[30][1] - (land[21][1]+land[22][1])/2)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img.save('icon/thug_r.png')

                    thug = PhotoImage(file = 'icon/thug_r.png')
                    canvas.create_image((land[21][0]+land[22][0])/2,land[27][1]+8, image = thug)
                    canvas.thug = thug
                    
                    thug1 = PhotoImage(file = 'icon/thug1.png')
                    canvas.create_image(land[56][0],land[56][1], image = thug1)
                    canvas.thug1 = thug1 
                    
                    health = PhotoImage(file = 'icon/health1.png')
                    canvas.create_image(240,475,image = health)
                    canvas.health = health
                    
                elif filter_code == 5:
                    img = Image.open('icon/mustache.png')
                    new_width  = int(land[54][0] - land[48][0]) + 30
                    new_height = int(land[51][1] - land[33][1]) + 15
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img.save('icon/mustache_r.png')

                    mustache = PhotoImage(file = 'icon/mustache_r.png')
                    canvas.create_image(int((land[33][0]+land[51][0])/2),int((land[33][1] + land[51][1])/2), image = mustache)
                    canvas.mustache = mustache
                    
            except:
                pass
            
            canvas.after(10, video)
        
        canvas = Canvas(root, width = 480, height = 480)
        canvas.pack()
        
        Filter()
        video()
        
        root.mainloop()  
        cam.release()
   
if __name__ == '__main__':
    Home()

root.mainloop()
