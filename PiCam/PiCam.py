#!/usr/bin/python
# -*- coding: utf-8 -*-


###  Copyright (C) 2021 4bitFox  ###


#Basic Camera UI for the Raspberry Pi.
#I wrote it for the Raspberry Pi HQ Camera on a Rasberry Pi 4B, with a small LCD on top.
#If you use a different camera module you will have to adjust some settings (e.g. the Sensor Mode). Same when you use a different res display ect...
#I'm new to programming, so the code could probably be better and some things are hacky (Filename-date, simulated keypresses and image viewing with feh). It works fine for what I want to use it for tough.

#This script requires "qt5-default" and "feh" to be installed!
#You also need to have these libraries installed (PyQt5, qpiozero, pynput):
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from gpiozero import Button
from pynput.keyboard import Key, Controller
from time import sleep
import os
import datetime
import sys 


##Settings##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#This script uses raspistill. 
#Search the documentation or use "raspistill --help" for possible options:
#https://www.raspberrypi.org/documentation/raspbian/applications/camera.md

#Screen & Preview dimentions in pixels
#If you have to change this, you'll probably have to adjust the font-sizes in the code below by yourself! 
#Button boundaries will scale automatically.
wscreen  = 480 #Screen width
hscreen  = 320 #Screen height
wpreview = 427 #Preview width


#Output settings
setting_output_location = "~/Pictures/" #Where to store pictures
setting_output_prefix = "IMG_"          #Filename prefix
setting_output_suffix_noraw = "N"       #Filename suffix when RAW disabled
setting_output_suffix_raw = "R"         #Filename suffix when RAW enabled
setting_encoding = "jpg"                #Encoding of picture taken
setting_mode = 3                        #Sensor mode
setting_quality = 90                    #Compression quality
setting_thumbnail = "64,48,35"          #Thumbnail settings ("width,height,quality")


#Default Camera settings
setting_ISO = 0        #ISO
setting_AWB = "auto"   #Auto White Balance
setting_SS  = 0        #Shutter Speed
setting_EXP = "auto"   #Exposure Mode
setting_EXM = "matrix" #Exposure Metering
#Default additional settings
setting_FoM     = False   #Display focus FoM value
setting_raw     = True   #Add raw Bayer data to JPEG
setting_flicker = "50hz" #Flicker avoidance
setting_hf      = False  #Flip Image horizontally
setting_vf      = False  #Flip Image vertically


#GPIO Buttons
#If you use buttons connected to GPIO, you can set the pin numbers here:
button_capture = Button(21) #Take a photo
button_up      = Button(25) #Move up in menu
button_select  = Button(23) #Select in menu
button_down    = Button(24) #Move down in menu

#Other
style = "line" #How the UI looks. You can use "boxes" or "lines"
debugging = True #Debugging (print stuff to console)


### The "real" code beginns here :) ###
##Shorten common Variables, Save initial setting & other stuff##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
w = wscreen - wpreview #Empty space left for window
h = hscreen

setting_flicker_init = setting_flicker
if setting_flicker_init == "off":
    setting_flicker_init_bool = False
else:
    setting_flicker_init_bool = True
    
xdist_style = 5

##Debug & Info##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def print_settings(debug):
    if debug:
        print("##Picture Settings:##")
        if setting_ISO == 0:
            print("ISO: auto")
        else:
            print("ISO:", setting_ISO)
        print("AWB:", setting_AWB)
        if setting_SS == 0:
            print("SS:  auto")
        else:
            print("SS: ", setting_SS, "µs")
        print("EXP:", setting_EXP)
        print("EXM:", setting_EXM)
        print("")
        print("##Additional Settings:##")
        print("FoM:         ", setting_FoM)
        print("raw Bayer:   ", setting_raw)
        print("Anti-Flicker:", setting_flicker)
        print("H Flip:      ", setting_hf)
        print("V Flip:      ", setting_vf)
        print()

print_settings(debugging)


##WINDOW CLASS##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Window(QMainWindow): 
    def __init__(self):
        #Window properties
        super().__init__()
        
        global xdist_style
        
        self.setWindowTitle("PiCam") 
        self.setGeometry(0, 0, wscreen, h)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        if style == "boxes":
            xdist_style = 5
            stylesheet = """
            QWidget {
            background-color: black;
            }
    
            QPushButton {
            border: 1px solid gray;
            color: white;
            }
        
            QPushButton:focus {
            border: 2px solid gray;
            }
        
            QPushButton:pressed {
            background-color: gray;
            }
        
            QCheckBox {
            border: 1px solid gray;
            color: white;
            }
        
            QCheckBox:focus {
            border: 2px solid gray;
            }
        
            QCheckBox:pressed {
            background-color: gray;
            }
        
            QCheckBox:checked {
            color: green;
            }
        
            QCheckBox:unchecked {
            color: red;
            }
        
            QCheckBox::indicator {
            width: 0px;
            height: 0px;
            }
            """
        
        if style == "line":
            xdist_style = 2
            stylesheet = """
            QWidget {
            background-color: black;
            }
    
            QPushButton {
            border: 2px solid;
            border-left-color: lightgray;
            border-right-color: black;
            border-top-color: black;
            border-bottom-color: black;
            color: white;
            }
        
            QPushButton:focus {
            border: 4px solid;
            border-left-color: white;
            }
        
            QPushButton:pressed {
            border: 3px solid;
            border-left-color: gray;
            }
        
            QCheckBox {
            border: 2px solid;
            border-left-color: lightgray;
            border-right-color: black;
            border-top-color: black;
            border-bottom-color: black;
            color: white;
            }
        
            QCheckBox:focus {
            border: 4px solid;
            border-left-color: white;
            }
        
            QCheckBox:pressed {
            border: 3px solid;
            border-left-color: gray;
            }
        
            QCheckBox:checked {
            color: green;
            }
        
            QCheckBox:unchecked {
            color: red;
            }
        
            QCheckBox::indicator {
            width: 0px;
            height: 0px;
            }
            """

        self.setStyleSheet(stylesheet)
        
    
    #Create Button
    def button(self, x, y, w, h, Label, font_size, Command, visibility):
        button = QPushButton(Label, self)
        button.move(x, y)
        button.resize(w, h)
        button.clicked.connect(Command)
        button.setFont(QFont("Arial", font_size))
        if not visibility:
            button.hide()
            
        return button
    
    #Create CheckBox
    def checkbox(self, x, y, w, h, Label, font_size, State, Command, visibility):
        checkbox = QCheckBox(Label, self)
        checkbox.move(x, y)
        checkbox.resize(w, h)
        checkbox.setChecked(State)
        checkbox.stateChanged.connect(Command)
        checkbox.setFont(QFont("Arial", font_size))
        if not visibility:
            checkbox.hide()
            
        return checkbox


##Create window##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
App = QApplication(sys.argv)
Menu = Window()


##Button pressed actions##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#Button action Main Menu
def button_ISO_pressed():
    visibility_Menu(False)
    visibility_Menu_ISO(True)
def button_AWB_pressed():
    visibility_Menu(False)
    visibility_Menu_AWB(True)
def button_SS_pressed():
    visibility_Menu(False)
    visibility_Menu_SS_1(True)
def button_EXP_pressed():
    visibility_Menu(False)
    visibility_Menu_EXP(True)
def button_ETC_pressed():
    visibility_Menu_ETC(True)
    visibility_Menu(False)


#Button action ISO Menu
def button_ISO_any_act(value):
    global setting_ISO
    setting_ISO = value
    visibility_Menu_ISO(False)
    visibility_Menu(True)


#Button action AWB Menu
def button_AWB_any_act(mode):
    global setting_AWB
    setting_AWB = mode
    visibility_Menu_AWB(False)
    visibility_Menu(True)


#Button action SS Menu 1
def button_SS_UP_1_pressed():
    visibility_Menu_SS_1(False)
    visibility_Menu_SS_3(True)
def button_SS_DOWN_1_pressed():
    visibility_Menu_SS_1(False)
    visibility_Menu_SS_2(True)
def button_SS_1_act(value):
    global setting_SS
    setting_SS = value
    visibility_Menu_SS_1(False)
    visibility_Menu(True)
    
#Button action SS Menu 2
def button_SS_UP_2_pressed():
    visibility_Menu_SS_2(False)
    visibility_Menu_SS_1(True)
def button_SS_DOWN_2_pressed():
    visibility_Menu_SS_2(False)
    visibility_Menu_SS_3(True)
def button_SS_2_act(value):
    global setting_SS
    setting_SS = value
    visibility_Menu_SS_2(False)
    visibility_Menu(True)
    
#Button action SS Menu 3
def button_SS_UP_3_pressed():
    visibility_Menu_SS_3(False)
    visibility_Menu_SS_2(True)
def button_SS_DOWN_3_pressed():
    visibility_Menu_SS_3(False)
    visibility_Menu_SS_1(True)
def button_SS_3_act(value):
    global setting_SS
    setting_SS = value
    visibility_Menu_SS_3(False)
    visibility_Menu(True)


#Button action EXP Menu
def button_EXP_mode_pressed(): #Switch menu
    visibility_Menu_EXP(False)
    visibility_Menu_EXP_Mode(True)
def button_EXM_any_act(mode):
    global setting_EXM
    setting_EXM = mode
    visibility_Menu_EXP(False)
    visibility_Menu(True)


#Button action EXP Mode Menu
def button_EXP_any_act(mode):
    global setting_EXP
    setting_EXP = mode
    visibility_Menu_EXP_Mode(False)
    visibility_Menu(True)
    

#Button action ETC Menu
def button_ETC_PIC_pressed():
    visibility_Menu_ETC(False)
    feh()
    visibility_Menu_PIC(True)
def button_ETC_BACK_pressed():
    visibility_Menu_ETC(False)
    visibility_Menu(True)
    

#Button action PIC Menu
def button_PIC_next_pressed():
    simulate_button_PIC_next_pressed()
    Menu.activateWindow()
def button_PIC_prev_pressed():
    simulate_button_PIC_prev_pressed()
    Menu.activateWindow()
def button_PIC_rotr_pressed():
    simulate_button_PIC_rotr_pressed()
    Menu.activateWindow()
def button_PIC_rotl_pressed():
    simulate_button_PIC_rotl_pressed()
    Menu.activateWindow()
def button_PIC_BAK_pressed():
    visibility_Menu_PIC(False)
    raspistill()
    visibility_Menu(True)
    

##CheckBox checked actions##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#CheckBox action ETC FoM
def checkbox_ETC_FoM_pressed():
    global setting_FoM
    setting_FoM = not setting_FoM
#CheckBox action ETC raw
def checkbox_ETC_raw_pressed():
    global setting_raw
    setting_raw = not setting_raw
#CheckBox action ETC flicker avoidance
def checkbox_ETC_flicker_pressed():
    global setting_flicker
    global setting_flicker_init
    if setting_flicker == "50hz" or setting_flicker == "60hz" or setting_flicker == "auto":
        setting_flicker = "off"
    else:
        setting_flicker = setting_flicker_init
#CheckBox action ETC horizontal flip
def checkbox_ETC_hf_pressed():
    global setting_hf
    setting_hf = not setting_hf
#CheckBox action ETC vertical flip
def checkbox_ETC_vf_pressed():
    global setting_vf
    setting_vf = not setting_vf


##Create menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
xdist = xdist_style
ydist = 20
button_w = w - xdist * 2
button_h = h/8
button_dist = button_h + h/24
#Create buttons for Main Menu
button_ISO = Menu.button(xdist, ydist + button_dist*0, button_w, button_h, "ISO", 12, button_ISO_pressed, True)
button_AWB = Menu.button(xdist, ydist + button_dist*1, button_w, button_h, "AWB", 12, button_AWB_pressed, True)
button_SS  = Menu.button(xdist, ydist + button_dist*2, button_w, button_h,  "SS", 12,  button_SS_pressed, True)
button_EXP = Menu.button(xdist, ydist + button_dist*3, button_w, button_h, "EXP", 12, button_EXP_pressed, True)
button_ETC = Menu.button(xdist,  h - ydist - button_h, button_w, button_h,   "⚙", 20, button_ETC_pressed, True)
#Change visibility of Main Menu
def visibility_Menu(visibility):
    if visibility:
        button_ISO.show()
        button_AWB.show()
        button_SS.show()
        button_EXP.show()
        button_ETC.show()
        button_ISO.setFocus() #Set Focus
        print_settings(debugging) #Print changed settings to console
        raspistill() #Refresh preview
    else:
        button_ISO.hide()
        button_AWB.hide()
        button_SS.hide()
        button_EXP.hide()
        button_ETC.hide()


##Create ISO menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
button_ISO_h = h/11
button_ISO_dist = (h - 2*ydist - button_ISO_h)/7
#Create buttons for ISO Menu
button_ISO_auto = Menu.button(xdist, ydist + button_ISO_dist*0, button_w, button_ISO_h, "AUTO", 10, lambda: button_ISO_any_act(0),   False)
button_ISO_100  = Menu.button(xdist, ydist + button_ISO_dist*1, button_w, button_ISO_h,  "100", 12, lambda: button_ISO_any_act(100), False)
button_ISO_200  = Menu.button(xdist, ydist + button_ISO_dist*2, button_w, button_ISO_h,  "200", 12, lambda: button_ISO_any_act(200), False)
button_ISO_320  = Menu.button(xdist, ydist + button_ISO_dist*3, button_w, button_ISO_h,  "320", 12, lambda: button_ISO_any_act(320), False)
button_ISO_400  = Menu.button(xdist, ydist + button_ISO_dist*4, button_w, button_ISO_h,  "400", 12, lambda: button_ISO_any_act(400), False)
button_ISO_500  = Menu.button(xdist, ydist + button_ISO_dist*5, button_w, button_ISO_h,  "500", 12, lambda: button_ISO_any_act(500), False)
button_ISO_640  = Menu.button(xdist, ydist + button_ISO_dist*6, button_w, button_ISO_h,  "640", 12, lambda: button_ISO_any_act(640), False)
button_ISO_800  = Menu.button(xdist, ydist + button_ISO_dist*7, button_w, button_ISO_h,  "800", 12, lambda: button_ISO_any_act(800), False)
#Change visibility of ISO Menu
def visibility_Menu_ISO(visibility):
    if visibility:
        button_ISO_auto.show()
        button_ISO_100.show()
        button_ISO_200.show()
        button_ISO_320.show()
        button_ISO_400.show()
        button_ISO_500.show()
        button_ISO_640.show()
        button_ISO_800.show()
        button_ISO_auto.setFocus() #Set Focus
    else:
        button_ISO_auto.hide()
        button_ISO_100.hide()
        button_ISO_200.hide()
        button_ISO_320.hide()
        button_ISO_400.hide()
        button_ISO_500.hide()
        button_ISO_640.hide()
        button_ISO_800.hide()


##Create AWB menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
button_AWB_h = h/12
button_AWB_dist = (h - 2*ydist - button_AWB_h)/8
#Create buttons for AWB Menu
button_AWB_auto         = Menu.button(xdist, ydist + button_AWB_dist*0, button_w, button_AWB_h, "AUTO", 10, lambda: button_AWB_any_act("auto"),         False)
button_AWB_sunlight     = Menu.button(xdist, ydist + button_AWB_dist*1, button_w, button_AWB_h,    "☀", 16, lambda: button_AWB_any_act("sun"),          False)
button_AWB_cloudy       = Menu.button(xdist, ydist + button_AWB_dist*2, button_w, button_AWB_h,    "☁", 16, lambda: button_AWB_any_act("cloud"),        False)
button_AWB_shade        = Menu.button(xdist, ydist + button_AWB_dist*3, button_w, button_AWB_h,    "▧", 14, lambda: button_AWB_any_act("shade"),        False)
button_AWB_tungsten     = Menu.button(xdist, ydist + button_AWB_dist*4, button_w, button_AWB_h,    "W", 12, lambda: button_AWB_any_act("tungsten"),     False)
button_AWB_fluorescent  = Menu.button(xdist, ydist + button_AWB_dist*5, button_w, button_AWB_h,    "F", 12, lambda: button_AWB_any_act("fluorescent"),  False)
button_AWB_incandescent = Menu.button(xdist, ydist + button_AWB_dist*6, button_w, button_AWB_h,    "I", 12, lambda: button_AWB_any_act("incandescent"), False)
button_AWB_flash        = Menu.button(xdist, ydist + button_AWB_dist*7, button_w, button_AWB_h,    "⚡", 16, lambda: button_AWB_any_act("flash"),        False)
button_AWB_horizon      = Menu.button(xdist, ydist + button_AWB_dist*8, button_w, button_AWB_h,    "♎", 16, lambda: button_AWB_any_act("horizon"),      False)
#Change visibility of AWB Menu
def visibility_Menu_AWB(visibility):
    if visibility:
        button_AWB_auto.show()
        button_AWB_sunlight.show()
        button_AWB_cloudy.show()
        button_AWB_shade.show()
        button_AWB_tungsten.show()
        button_AWB_fluorescent.show()
        button_AWB_incandescent.show()
        button_AWB_flash.show()
        button_AWB_horizon.show()
        button_AWB_auto.setFocus() #Set Focus
    else:
        button_AWB_auto.hide()
        button_AWB_sunlight.hide()
        button_AWB_cloudy.hide()
        button_AWB_shade.hide()
        button_AWB_tungsten.hide()
        button_AWB_fluorescent.hide()
        button_AWB_incandescent.hide()
        button_AWB_flash.hide()
        button_AWB_horizon.hide()


##Create SS menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
button_SS_h = h/12
button_SS_dist = (h - 2*ydist - button_SS_h)/8
#Create buttons for SS Menu 1
button_SS_UP_1     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_1_pressed,            False)
button_SS_1000     = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h, "1/1000", 10, lambda: button_SS_1_act(1000),     False)
button_SS_2000     = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,  "1/500", 10, lambda: button_SS_1_act(2000),     False)
button_SS_4000     = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,  "1/250", 10, lambda: button_SS_1_act(4000),     False)
button_SS_8000     = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,  "1/125", 10, lambda: button_SS_1_act(8000),     False)
button_SS_16667    = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h,   "1/60", 10, lambda: button_SS_1_act(16667),    False)
button_SS_33333    = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h,   "1/30", 10, lambda: button_SS_1_act(33333),    False)
button_SS_66667    = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h,   "1/15", 10, lambda: button_SS_1_act(66667),    False)
button_SS_DOWN_1   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_1_pressed,          False)
#Create buttons for SS Menu 2
button_SS_UP_2     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_2_pressed,            False)
button_SS_125000   = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h,    "1/8", 10, lambda: button_SS_2_act(125000),   False)
button_SS_250000   = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,    "1/4", 10, lambda: button_SS_2_act(250000),   False)
button_SS_500000   = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,    "1/2", 10, lambda: button_SS_2_act(500000),   False)
button_SS_1000000  = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,      "1", 10, lambda: button_SS_2_act(1000000),  False)
button_SS_2000000  = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h,      "2", 10, lambda: button_SS_2_act(2000000),  False)
button_SS_4000000  = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h,      "4", 10, lambda: button_SS_2_act(4000000),  False)
button_SS_8000000  = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h,      "8", 10, lambda: button_SS_2_act(8000000),  False)
button_SS_DOWN_2   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_2_pressed,          False)
#Create buttons for SS Menu 3
button_SS_UP_3     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_3_pressed,            False)
button_SS_15000000 = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h,     "15", 10, lambda: button_SS_3_act(15000000), False)
button_SS_30000000 = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,     "30", 10, lambda: button_SS_3_act(30000000), False)
button_SS_60000000 = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,     "60", 10, lambda: button_SS_3_act(60000000), False)
button_SS_auto     = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,   "AUTO", 10, lambda: button_SS_3_act(0),        False)
button_SS_125      = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h, "1/8000", 10, lambda: button_SS_3_act(125),      False)
button_SS_250      = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h, "1/4000", 10, lambda: button_SS_3_act(250),      False)
button_SS_500      = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h, "1/2000", 10, lambda: button_SS_3_act(500),      False)
button_SS_DOWN_3   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_3_pressed,          False)
#Change visibility of SS Menu 1
def visibility_Menu_SS_1(visibility):
    if visibility:
        button_SS_UP_1.show()
        button_SS_1000.show()
        button_SS_2000.show()
        button_SS_4000.show()
        button_SS_8000.show()
        button_SS_16667.show()
        button_SS_33333.show()
        button_SS_66667.show()
        button_SS_DOWN_1.show()
        button_SS_8000.setFocus() #Set Focus
    else:
        button_SS_UP_1.hide()
        button_SS_1000.hide()
        button_SS_2000.hide()
        button_SS_4000.hide()
        button_SS_8000.hide()
        button_SS_16667.hide()
        button_SS_33333.hide()
        button_SS_66667.hide()
        button_SS_DOWN_1.hide()
#Change visibility of SS Menu 2
def visibility_Menu_SS_2(visibility):
    if visibility:
        button_SS_UP_2.show()
        button_SS_125000.show()
        button_SS_250000.show()
        button_SS_500000.show()
        button_SS_1000000.show()
        button_SS_2000000.show()
        button_SS_4000000.show()
        button_SS_8000000.show()
        button_SS_DOWN_2.show()
        button_SS_1000000.setFocus() #Set Focus
    else:
        button_SS_UP_2.hide()
        button_SS_125000.hide()
        button_SS_250000.hide()
        button_SS_500000.hide()
        button_SS_1000000.hide()
        button_SS_2000000.hide()
        button_SS_4000000.hide()
        button_SS_8000000.hide()
        button_SS_DOWN_2.hide()
#Change visibility of SS Menu 3
def visibility_Menu_SS_3(visibility):
    if visibility:
        button_SS_UP_3.show()
        button_SS_15000000.show()
        button_SS_30000000.show()
        button_SS_60000000.show()
        button_SS_auto.show()
        button_SS_125.show()
        button_SS_250.show()
        button_SS_500.show()
        button_SS_DOWN_3.show()
        button_SS_auto.setFocus() #Set Focus
    else:
        button_SS_UP_3.hide()
        button_SS_15000000.hide()
        button_SS_30000000.hide()
        button_SS_60000000.hide()
        button_SS_auto.hide()
        button_SS_125.hide()
        button_SS_250.hide()
        button_SS_500.hide()
        button_SS_DOWN_3.hide()
        

##Create EXP menus##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
button_EXM_h = h/8
button_EXM_dist = button_EXM_h + h/24
button_EXP_h = h/12
button_EXP_dist = (h - 2*ydist - button_EXP_h)/8
#Create buttons for EXP (Metering) Menu
button_EXM_average   = Menu.button(xdist, ydist + button_EXM_dist*0, button_w, button_EXM_h,    "∅", 22, lambda: button_EXM_any_act("average"),   False)
button_EXM_matrix    = Menu.button(xdist, ydist + button_EXM_dist*1, button_w, button_EXM_h,    "◯", 16, lambda: button_EXM_any_act("matrix"),    False)
button_EXM_spot      = Menu.button(xdist, ydist + button_EXM_dist*2, button_w, button_EXM_h,    "·", 18, lambda: button_EXM_any_act("spot"),      False)
button_EXM_backlit   = Menu.button(xdist, ydist + button_EXM_dist*3, button_w, button_EXM_h,   "⚞I", 18, lambda: button_EXM_any_act("backlit"),   False)
button_EXP_mode      = Menu.button(xdist,  h - ydist - button_EXM_h, button_w, button_EXM_h, "MODE", 10, button_EXP_mode_pressed,                 False)
#Create buttons for EXP Mode Menu (nested)
button_EXP_auto      = Menu.button(xdist, ydist + button_EXP_dist*0, button_w, button_EXP_h, "AUTO", 10, lambda: button_EXP_any_act("auto"),      False)
button_EXP_night     = Menu.button(xdist, ydist + button_EXP_dist*1, button_w, button_EXP_h,   " ☾", 16, lambda: button_EXP_any_act("night"),     False)
button_EXP_backlight = Menu.button(xdist, ydist + button_EXP_dist*2, button_w, button_EXP_h,   "⚞I", 12, lambda: button_EXP_any_act("backlight"), False)
button_EXP_spotlight = Menu.button(xdist, ydist + button_EXP_dist*3, button_w, button_EXP_h,    "☄", 16, lambda: button_EXP_any_act("spotlight"), False)
button_EXP_sports    = Menu.button(xdist, ydist + button_EXP_dist*4, button_w, button_EXP_h,    "☡", 14, lambda: button_EXP_any_act("sports"),    False)
button_EXP_snow      = Menu.button(xdist, ydist + button_EXP_dist*5, button_w, button_EXP_h,    "☃", 18, lambda: button_EXP_any_act("snow"),      False)
button_EXP_beach     = Menu.button(xdist, ydist + button_EXP_dist*6, button_w, button_EXP_h,    "≃", 16, lambda: button_EXP_any_act("beach"),     False)
button_EXP_fireworks = Menu.button(xdist, ydist + button_EXP_dist*7, button_w, button_EXP_h,    "≛", 16, lambda: button_EXP_any_act("fireworks"), False)
button_EXP_antishake = Menu.button(xdist, ydist + button_EXP_dist*8, button_w, button_EXP_h,  "░▒▓",  8, lambda: button_EXP_any_act("antishake"), False)
#Change visibility of EXP Menu
def visibility_Menu_EXP(visibility):
    if visibility:
        button_EXM_average.show()
        button_EXM_matrix.show()
        button_EXM_spot.show()
        button_EXM_backlit.show()
        button_EXP_mode.show()
        button_EXM_matrix.setFocus() #Set Focus
    else:
        button_EXM_average.hide()
        button_EXM_matrix.hide()
        button_EXM_spot.hide()
        button_EXM_backlit.hide()
        button_EXP_mode.hide()
#Cange visibility of EXP Mode Menu (nested)
def visibility_Menu_EXP_Mode(visibility):
    if visibility:
        button_EXP_auto.show()
        button_EXP_night.show()
        button_EXP_backlight.show()
        button_EXP_spotlight.show()
        button_EXP_sports.show()
        button_EXP_snow.show()
        button_EXP_beach.show()
        button_EXP_fireworks.show()
        button_EXP_antishake.show()
        button_EXP_auto.setFocus() #Set Focus
    else:
        button_EXP_auto.hide()
        button_EXP_night.hide()
        button_EXP_backlight.hide()
        button_EXP_spotlight.hide()
        button_EXP_sports.hide()
        button_EXP_snow.hide()
        button_EXP_beach.hide()
        button_EXP_fireworks.hide()
        button_EXP_antishake.hide()


##Create ECT menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
checkbox_w = button_w
checkbox_h = h/12
checkbox_ETC_dist = checkbox_h + h/50
button_ETC_h = h/8
button_ETC_dist = button_ETC_h + h/24
checkbox_ETC_FoM     = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*0, checkbox_w, checkbox_h, "FoM", 10, setting_FoM,               checkbox_ETC_FoM_pressed,     False)
checkbox_ETC_raw     = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*1, checkbox_w, checkbox_h, "RAW", 10, setting_raw,               checkbox_ETC_raw_pressed,     False)
checkbox_ETC_flicker = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*2, checkbox_w, checkbox_h,  "Hz", 12, setting_flicker_init_bool, checkbox_ETC_flicker_pressed, False)
checkbox_ETC_hf      = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*3, checkbox_w, checkbox_h,  "HF", 12, setting_hf,                checkbox_ETC_hf_pressed,      False)
checkbox_ETC_vf      = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*4, checkbox_w, checkbox_h,  "VF", 12, setting_vf,                checkbox_ETC_vf_pressed,      False)
button_ETC_PIC       = Menu.button(xdist, h - ydist - button_ETC_h - button_ETC_dist*1, button_w, button_ETC_h, "PIC", 12, button_ETC_PIC_pressed,  False)
button_ETC_BACK      = Menu.button(xdist, h - ydist - button_ETC_h - button_ETC_dist*0, button_w, button_ETC_h,   "↩", 24, button_ETC_BACK_pressed, False)
#Change visibility of ETC Menu
def visibility_Menu_ETC(visibility):
    if visibility:
        checkbox_ETC_FoM.show()
        checkbox_ETC_raw.show()
        checkbox_ETC_flicker.show()
        checkbox_ETC_hf.show()
        checkbox_ETC_vf.show()
        button_ETC_PIC.show()
        button_ETC_BACK.show()
        button_ETC_PIC.setFocus() #Set Focus
    else:
        checkbox_ETC_FoM.hide()
        checkbox_ETC_raw.hide()
        checkbox_ETC_flicker.hide()
        checkbox_ETC_hf.hide()
        checkbox_ETC_vf.hide()
        button_ETC_PIC.hide()
        button_ETC_BACK.hide()


##Create PIC menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
button_PIC_h = h/8
button_PIC_dist = button_PIC_h + h/24
#Create buttons for PIC (Metering) Menu
button_PIC_next = Menu.button(xdist, ydist + button_PIC_dist*0, button_w, button_PIC_h, "►", 12, button_PIC_next_pressed,   False)
button_PIC_prev = Menu.button(xdist, ydist + button_PIC_dist*1, button_w, button_PIC_h, "◄", 12, button_PIC_prev_pressed,   False)
button_PIC_rotr = Menu.button(xdist, ydist + button_PIC_dist*2, button_w, button_PIC_h, "↻", 20, button_PIC_rotr_pressed,   False)
button_PIC_rotl = Menu.button(xdist, ydist + button_PIC_dist*3, button_w, button_PIC_h, "↺", 20, button_PIC_rotl_pressed,   False)
button_PIC_BAK  = Menu.button(xdist,  h - ydist - button_PIC_h, button_w, button_PIC_h, "↩", 24, button_PIC_BAK_pressed,    False)
#Change visibility of PIC Menu
def visibility_Menu_PIC(visibility):
    if visibility:
        button_PIC_next.show()
        button_PIC_prev.show()
        button_PIC_rotr.show()
        button_PIC_rotl.show()
        button_PIC_BAK.show()
        button_PIC_next.setFocus() #Set Focus
    else:
        button_PIC_next.hide()
        button_PIC_prev.hide()
        button_PIC_rotr.hide()
        button_PIC_rotl.hide()
        button_PIC_BAK.hide()


##CAMERA##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#Make raspistill command
def raspistill_command():
    #Output
    year = datetime.date.today().year
    month = datetime.date.today().month
    if month < 10:
        arg_output_prefix = setting_output_prefix + str(year) + "0"
    else:
        arg_output_prefix = setting_output_prefix + str(year)
    if setting_raw:
        arg_output_suffix = setting_output_suffix_raw
    else:
        arg_output_suffix = setting_output_suffix_noraw
    
    #Arguments
    arg_needed = "-t 0 -dt -s "
    
    arg_preview   = "-p "  + str(w) + ",0," + str(wpreview) + "," + str(h) + " "
    arg_output    = "-o "  + setting_output_location + arg_output_prefix + "%d" + arg_output_suffix + "." + setting_encoding + " "
    arg_encoding  = "-e "  + setting_encoding     + " "
    arg_mode      = "-md " + str(setting_mode)    + " "
    arg_quality   = "-q "  + str(setting_quality) + " "
    arg_thumbnail = "-th " + setting_thumbnail    + " "
    
    arg_ISO = "-ISO " + str(setting_ISO) + " "
    arg_AWB = "-awb " + str(setting_AWB) + " "
    arg_SS  = "-ss "  + str(setting_SS)  + " "
    arg_EXP = "-ex "  + str(setting_EXP) + " "
    arg_EXM = "-mm "  + str(setting_EXM) + " "
    
    arg_FoM     = "-fw "
    arg_raw     = "-r "
    arg_flicker = "-fli " + str(setting_flicker) + " "
    arg_hf      = "-hf "
    arg_vf      = "-vf "
    
    
    #Make Command
    command  = "raspistill "
    command += arg_needed
    command += arg_preview
    command += arg_output
    command += arg_encoding
    command += arg_mode
    command += arg_quality
    command += arg_thumbnail
    command += arg_ISO
    command += arg_AWB
    command += arg_SS
    command += arg_EXP
    command += arg_EXM
    if setting_FoM:
        command += arg_FoM
    if setting_raw:
        command += arg_raw
    command += arg_flicker
    if setting_hf:
        command += arg_hf
    if setting_vf:
        command += arg_vf
    #Debugging message
    if debugging:
        print("##raspistill command:##")
        print(command)
        print("")
        
    return command + "&"

#Launch (or) relaunch raspistill. Needs to be run each time camera settings change
def raspistill():
    os.system("pkill feh")
    os.system("pkill raspistill")
    Menu.setGeometry(0, 0, wscreen, h)
    raspistill = raspistill_command()
    os.system(raspistill)

#capture image
def capture():
    os.system("pkill -USR1 raspistill")
    #Debugging message
    if debugging:
        print("Image captured")


##Image viever##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#Make feh command
def feh_command():
    arg_path = setting_output_location + " "
    arg_geometry = "-x -g " + str(wpreview) + "x" + str(h) + "+" + str(w) + "+0 -. "
    arg_needed = "-n -d -B black -N --edit "
    
    command  = "feh "
    command += arg_path
    command += arg_geometry
    command += arg_needed
    #Debugging message
    if debugging:
        print("##feh command:##")
        print(command)
        print("")
    
    return command + "&"


def feh():
    os.system("pkill raspistill")
    feh = feh_command()
    os.system(feh)
    sleep(2)#Increrase if feh takes long to open
    Menu.setGeometry(0, 0, w, h)
    Menu.activateWindow()


##GPIO & Keys##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
keyboard = Controller()
#Shoot picture button
def gpio_button_capture_pressed():
    capture()
#Simulate the correct Keypresses from GPIO
def gpio_button_up_pressed():
    keyboard.press(Key.up)
    keyboard.release(Key.up)
def gpio_button_select_pressed():
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    sleep(0.2) #Prevent accidental "double press"
def gpio_button_down_pressed():
    keyboard.press(Key.down)
    keyboard.release(Key.down)

#Test for GPIO button presses
button_capture.when_pressed = gpio_button_capture_pressed
button_up.when_pressed      = gpio_button_up_pressed
button_select.when_pressed  = gpio_button_select_pressed
button_down.when_pressed    = gpio_button_down_pressed

#Simulate Keypress from QPushButton
def simulate_alt_tab(): #Dirty workaround :)
    alt_tab_delay = 0.5
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.release(Key.alt)
    sleep(alt_tab_delay)
def simulate_button_PIC_next_pressed():
    simulate_alt_tab()
    keyboard.press(Key.right)
    keyboard.release(Key.right)
def simulate_button_PIC_prev_pressed():
    simulate_alt_tab()
    keyboard.press(Key.left)
    keyboard.release(Key.left)
def simulate_button_PIC_rotr_pressed():
    simulate_alt_tab()
    keyboard.press(">")
    keyboard.release(">")
def simulate_button_PIC_rotl_pressed():
    simulate_alt_tab()
    keyboard.press("<")
    keyboard.release("<")


##Run App##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
raspistill() #Preview
Menu.show()  #show UI
App.exec()   #Run UI
