from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
#from time import sleep
#import keyboard
import sys 

#Screen & Preview dimentions in pixels
wscreen  = 480 #Screen width
hscreen  = 320 #Screen height
wpreview = 427 #Preview width

#Default Camera settings
setting_ISO = 0        #ISO
setting_AWB = "auto"   #Auto White Balance
setting_SS  = 0        #Shutter Speed
setting_EXP = "auto"   #Exposure Mode
setting_EXM = "matrix" #Exposure Metering
#Default additional settings
setting_FoM     = True   #Display focus FoM value
setting_raw     = True   #Add raw Bayer data to JPEG
setting_flicker = "50hz" #Flicker avoidance
setting_hf      = False  #Flip Image horizontally
setting_vf      = False  #Flip Image vertically

debugging = True #Debugging (print stuff to console)


##Shorten common Variables, Save initial setting & other stuff##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
w = wscreen - wpreview #Empty space left for window
h = hscreen

setting_flicker_init = setting_flicker
if setting_flicker_init == "off":
    setting_flicker_init_bool = False
else:
    setting_flicker_init_bool = True

##Debug & Info##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def print_settings(debug):
    if debug:
        print("##Picture Settings##")
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
        print("##Additional Settings##")
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
        self.setWindowTitle("PiCam") 
        self.setGeometry(0, 0, wscreen, h)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: black;")
        
    #Create Button
    def button(self, x, y, w, h, Label, font_size, Command, visibility):
        button = QPushButton(Label, self)
        button.move(x, y)
        button.resize(w, h)
        button.clicked.connect(Command)
        button.setStyleSheet("border: 1px solid gray;" "color: white;")
        button.setFont(QFont("Arial", font_size))
        if not visibility:
            button.hide()
        return button
        
    #Create Label
    #def label(self, x, y, w, h, Label, visibility):
        #label = QLabel(self)
        #label.move(x, y)
        #label.resize(w, 20)
        #label.setText(Label)
        #label.setAlignment(Qt.AlignCenter)
        #label.setStyleSheet("border: 1px solid gray;" "color: white;")
        #if not visibility:
            #label.hide()
        #return label
    
    #Create CheckBox
    def checkbox(self, x, y, w, h, Label, font_size, State, Command, visibility):
        checkbox = QCheckBox(Label, self)
        checkbox.move(x, y)
        checkbox.resize(w, h)
        checkbox.setChecked(State)
        checkbox.stateChanged.connect(Command)
        checkbox.setStyleSheet("border: 1px solid gray;" "color: white;")
        checkbox.setFont(QFont("Arial", font_size))
        if not visibility:
            checkbox.hide()
        return checkbox

    #Create Slider
    #def slider(selfvmin, vmax, Interval, Step ,Value, Command, visibility):
        #slider = QSlider(Qt.Vertical, self)
        #slider.move(x, y)
        #slider.resize(w, h)
        #slider.setMinimum(vmin)
        #slider.setMaximum(vmax)
        #slider.setValue(Value)
        #slider.setTickPosition(QSlider.TicksBothSides)
        #slider.setTickInterval(Interval)
        #slider.setSingleStep(Step)
        #slider.valueChanged.connect(Command)
        #if not visibility:
            #slider.hide()
        #return slider


##Create window##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
App = QApplication(sys.argv)
Menu = Window()


##Button pressed actions##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#Button action Preview
def button_preview_pressed():
    pass


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
def button_ISO_auto_pressed():
    button_ISO_any_act(0)
def button_ISO_100_pressed():
    button_ISO_any_act(100)
def button_ISO_200_pressed():
    button_ISO_any_act(200)
def button_ISO_320_pressed():
    button_ISO_any_act(320)
def button_ISO_400_pressed():
    button_ISO_any_act(400)
def button_ISO_500_pressed():
    button_ISO_any_act(500)
def button_ISO_640_pressed():
    button_ISO_any_act(640)
def button_ISO_800_pressed():
    button_ISO_any_act(800)
def button_ISO_any_act(value): #act function
    global setting_ISO
    setting_ISO = value
    visibility_Menu_ISO(False)
    visibility_Menu(True)


#Button action AWB Menu
def button_AWB_auto_pressed():
    button_AWB_any_act("auto")
def button_AWB_sunlight_pressed():
    button_AWB_any_act("sunlight")
def button_AWB_cloudy_pressed():
    button_AWB_any_act("cloudy")
def button_AWB_shade_pressed():
    button_AWB_any_act("shade")
def button_AWB_tungsten_pressed():
    button_AWB_any_act("tungsten")
def button_AWB_fluorescent_pressed():
    button_AWB_any_act("fluorescent")
def button_AWB_incandescent_pressed():
    button_AWB_any_act("incandescent")
def button_AWB_flash_pressed():
    button_AWB_any_act("flash")
def button_AWB_horizon_pressed():
    button_AWB_any_act("horizon")
def button_AWB_any_act(mode): #act function
    global setting_AWB
    setting_AWB = mode
    visibility_Menu_AWB(False)
    visibility_Menu(True)


#Button action SS Menu 1
def button_SS_UP_1_pressed(): #UP
    visibility_Menu_SS_1(False)
    visibility_Menu_SS_3(True)
def button_SS_1000_pressed():
    button_SS_any_act(1, 1000)
def button_SS_2000_pressed():
    button_SS_any_act(1, 2000)
def button_SS_4000_pressed():
    button_SS_any_act(1, 4000)
def button_SS_8000_pressed():
    button_SS_any_act(1, 8000)
def button_SS_16667_pressed():
    button_SS_any_act(1, 16667)
def button_SS_33333_pressed():
    button_SS_any_act(1, 33333)
def button_SS_66667_pressed():
    button_SS_any_act(1, 66667)
def button_SS_DOWN_1_pressed(): #DOWN
    visibility_Menu_SS_1(False)
    visibility_Menu_SS_2(True)
#Button action SS Menu 2
def button_SS_UP_2_pressed(): #UP
    visibility_Menu_SS_2(False)
    visibility_Menu_SS_1(True)
def button_SS_125000_pressed():
    button_SS_any_act(2, 125000)
def button_SS_250000_pressed():
    button_SS_any_act(2, 250000)
def button_SS_500000_pressed():
    button_SS_any_act(2, 500000)
def button_SS_1000000_pressed():
    button_SS_any_act(2, 1000000)
def button_SS_2000000_pressed():
    button_SS_any_act(2, 2000000)
def button_SS_4000000_pressed():
    button_SS_any_act(2, 4000000)
def button_SS_8000000_pressed():
    button_SS_any_act(2, 8000000)
def button_SS_DOWN_2_pressed(): #DOWN
    visibility_Menu_SS_2(False)
    visibility_Menu_SS_3(True)
#Button action SS Menu 3
def button_SS_UP_3_pressed(): #UP
    visibility_Menu_SS_3(False)
    visibility_Menu_SS_2(True)
def button_SS_15000000_pressed():
    button_SS_any_act(3, 15000000)
def button_SS_30000000_pressed():
    button_SS_any_act(3, 30000000)
def button_SS_60000000_pressed():
    button_SS_any_act(3, 60000000)
def button_SS_auto_pressed():
    button_SS_any_act(3, 0)
def button_SS_125_pressed():
    button_SS_any_act(3, 125)
def button_SS_250_pressed():
    button_SS_any_act(3, 250)
def button_SS_500_pressed():
    button_SS_any_act(3, 500)
def button_SS_DOWN_3_pressed(): #DOWN
    visibility_Menu_SS_3(False)
    visibility_Menu_SS_1(True)
def button_SS_any_act(menu, value): #act function
    global setting_SS
    setting_SS = value
    if menu == 1:
        visibility_Menu_SS_1(False)
    elif menu == 2:
        visibility_Menu_SS_2(False)
    elif menu == 3:
        visibility_Menu_SS_3(False)
    visibility_Menu(True)


#Button action EXP Menu
def button_EXM_average_pressed():
    button_EXM_any_act("average")
def button_EXM_matrix_pressed():
    button_EXM_any_act("matrix")
def button_EXM_spot_pressed():
    button_EXM_any_act("spot")
def button_EXM_backlit_pressed():
    button_EXM_any_act("backlit")
def button_EXP_mode_pressed(): #Mode
    visibility_Menu_EXP(False)
    visibility_Menu_EXP_Mode(True)
def button_EXM_any_act(mode): #act function
    global setting_EXM
    setting_EXM = mode
    visibility_Menu_EXP(False)
    visibility_Menu(True)
#Button action EXP Mode Menu
def button_EXP_auto_pressed():
    button_EXP_any_act("auto")
def button_EXP_night_pressed():
    button_EXP_any_act("night")
def button_EXP_backlight_pressed():
    button_EXP_any_act("backlight")
def button_EXP_spotlight_pressed():
    button_EXP_any_act("spotlight")
def button_EXP_sports_pressed():
    button_EXP_any_act("sports")
def button_EXP_snow_pressed():
    button_EXP_any_act("snow")
def button_EXP_beach_pressed():
    button_EXP_any_act("beach")
def button_EXP_fireworks_pressed():
    button_EXP_any_act("fireworks")
def button_EXP_antishake_pressed():
    button_EXP_any_act("antishake")
def button_EXP_any_act(mode): #act function
    global setting_EXP
    setting_EXP = mode
    visibility_Menu_EXP_Mode(False)
    visibility_Menu(True)
    

#Button action ETC Menu
def button_ETC_PIC_pressed():
    visibility_Menu_ETC(False)
    visibility_Menu_PIC(True)
def button_ETC_BACK_pressed():
    visibility_Menu_ETC(False)
    visibility_Menu(True)
#Button action PIC Menu
def button_PIC_next_pressed():
    pass
def button_PIC_prev_pressed():
    pass
def button_PIC_rotate_pressed():
    pass
def button_PIC_save_pressed():
    pass
def button_PIC_BAK_pressed():
    visibility_Menu_PIC(False)
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


##Create Preview button##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#button_preview = Menu.button(w, 0, wpreview, h, "", 12, button_preview_pressed, True)


##Create menu##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
xdist = 5
ydist = 20
button_w = w - xdist * 2
button_h = h/8
button_dist = button_h + h/24
#Create buttons for Main Menu
button_ISO = Menu.button(xdist, ydist + button_dist*0, button_w, button_h, "ISO", 12, button_ISO_pressed, True)
button_AWB = Menu.button(xdist, ydist + button_dist*1, button_w, button_h, "AWB", 12, button_AWB_pressed, True)
button_SS  = Menu.button(xdist, ydist + button_dist*2, button_w, button_h,  "SS", 12,  button_SS_pressed, True)
button_EXP = Menu.button(xdist, ydist + button_dist*3, button_w, button_h, "EXP", 12, button_EXP_pressed, True)
button_ETC = Menu.button(xdist,  h - ydist - button_h, button_w, button_h, "✱", 16, button_ETC_pressed, True)
#Change visibility of Main Menu
def visibility_Menu(visibility):
    if visibility:
        button_ISO.show()
        button_AWB.show()
        button_SS.show()
        button_EXP.show()
        button_ETC.show()
        print_settings(debugging) #Print changed settings to console
        button_ISO.setFocus() #Set Focus
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
button_ISO_auto = Menu.button(xdist, ydist + button_ISO_dist*0, button_w, button_ISO_h, "AUTO", 10, button_ISO_auto_pressed, False)
button_ISO_100  = Menu.button(xdist, ydist + button_ISO_dist*1, button_w, button_ISO_h,  "100", 12,  button_ISO_100_pressed, False)
button_ISO_200  = Menu.button(xdist, ydist + button_ISO_dist*2, button_w, button_ISO_h,  "200", 12,  button_ISO_200_pressed, False)
button_ISO_320  = Menu.button(xdist, ydist + button_ISO_dist*3, button_w, button_ISO_h,  "320", 12,  button_ISO_320_pressed, False)
button_ISO_400  = Menu.button(xdist, ydist + button_ISO_dist*4, button_w, button_ISO_h,  "400", 12,  button_ISO_400_pressed, False)
button_ISO_500  = Menu.button(xdist, ydist + button_ISO_dist*5, button_w, button_ISO_h,  "500", 12,  button_ISO_500_pressed, False)
button_ISO_640  = Menu.button(xdist, ydist + button_ISO_dist*6, button_w, button_ISO_h,  "640", 12,  button_ISO_640_pressed, False)
button_ISO_800  = Menu.button(xdist, ydist + button_ISO_dist*7, button_w, button_ISO_h,  "800", 12,  button_ISO_800_pressed, False)
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
button_AWB_auto         = Menu.button(xdist, ydist + button_AWB_dist*0, button_w, button_AWB_h, "AUTO", 10, button_AWB_auto_pressed,         False)
button_AWB_sunlight     = Menu.button(xdist, ydist + button_AWB_dist*1, button_w, button_AWB_h,   "☀", 16, button_AWB_sunlight_pressed,     False)
button_AWB_cloudy       = Menu.button(xdist, ydist + button_AWB_dist*2, button_w, button_AWB_h,   "☁", 16, button_AWB_cloudy_pressed,       False)
button_AWB_shade        = Menu.button(xdist, ydist + button_AWB_dist*3, button_w, button_AWB_h,   "░░", 12, button_AWB_shade_pressed,        False)
button_AWB_tungsten     = Menu.button(xdist, ydist + button_AWB_dist*4, button_w, button_AWB_h,  " T💡", 12, button_AWB_tungsten_pressed,     False)
button_AWB_fluorescent  = Menu.button(xdist, ydist + button_AWB_dist*5, button_w, button_AWB_h,  " F💡", 12, button_AWB_fluorescent_pressed,  False)
button_AWB_incandescent = Menu.button(xdist, ydist + button_AWB_dist*6, button_w, button_AWB_h,  " I💡", 12, button_AWB_incandescent_pressed, False)
button_AWB_flash        = Menu.button(xdist, ydist + button_AWB_dist*7, button_w, button_AWB_h,    "ϟ", 16, button_AWB_flash_pressed,        False)
button_AWB_horizon      = Menu.button(xdist, ydist + button_AWB_dist*8, button_w, button_AWB_h,    "≐", 24, button_AWB_horizon_pressed,      False)
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
button_SS_UP_1     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_1_pressed,     False)
button_SS_1000     = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h, "1/1000", 10, button_SS_1000_pressed,     False)
button_SS_2000     = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,  "1/500", 10, button_SS_2000_pressed,     False)
button_SS_4000     = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,  "1/250", 10, button_SS_4000_pressed,     False)
button_SS_8000     = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,  "1/125", 10, button_SS_8000_pressed,     False)
button_SS_16667    = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h,   "1/60", 10, button_SS_16667_pressed,    False)
button_SS_33333    = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h,   "1/30", 10, button_SS_33333_pressed,    False)
button_SS_66667    = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h,   "1/15", 10, button_SS_66667_pressed,    False)
button_SS_DOWN_1   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_1_pressed,   False)
#Create buttons for SS Menu 2
button_SS_UP_2     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_2_pressed,     False)
button_SS_125000   = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h,    "1/8", 10, button_SS_125000_pressed,   False)
button_SS_250000   = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,    "1/4", 10, button_SS_250000_pressed,   False)
button_SS_500000   = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,    "1/2", 10, button_SS_500000_pressed,   False)
button_SS_1000000  = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,      "1", 10, button_SS_1000000_pressed,  False)
button_SS_2000000  = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h,      "2", 10, button_SS_2000000_pressed,  False)
button_SS_4000000  = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h,      "4", 10, button_SS_4000000_pressed,  False)
button_SS_8000000  = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h,      "8", 10, button_SS_8000000_pressed,  False)
button_SS_DOWN_2   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_2_pressed,   False)
#Create buttons for SS Menu 3
button_SS_UP_3     = Menu.button(xdist, ydist + button_SS_dist*0, button_w, button_SS_h,      "▲", 12, button_SS_UP_3_pressed,     False)
button_SS_15000000 = Menu.button(xdist, ydist + button_SS_dist*1, button_w, button_SS_h,     "15", 10, button_SS_15000000_pressed, False)
button_SS_30000000 = Menu.button(xdist, ydist + button_SS_dist*2, button_w, button_SS_h,     "30", 10, button_SS_30000000_pressed, False)
button_SS_60000000 = Menu.button(xdist, ydist + button_SS_dist*3, button_w, button_SS_h,     "60", 10, button_SS_60000000_pressed, False)
button_SS_auto     = Menu.button(xdist, ydist + button_SS_dist*4, button_w, button_SS_h,   "AUTO", 10, button_SS_auto_pressed,     False)
button_SS_125      = Menu.button(xdist, ydist + button_SS_dist*5, button_w, button_SS_h, "1/8000", 10, button_SS_125_pressed,      False)
button_SS_250      = Menu.button(xdist, ydist + button_SS_dist*6, button_w, button_SS_h, "1/4000", 10, button_SS_250_pressed,      False)
button_SS_500      = Menu.button(xdist, ydist + button_SS_dist*7, button_w, button_SS_h, "1/2000", 10, button_SS_500_pressed,      False)
button_SS_DOWN_3   = Menu.button(xdist, ydist + button_SS_dist*8, button_w, button_SS_h,      "▼", 12, button_SS_DOWN_3_pressed,   False)
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
button_EXM_average   = Menu.button(xdist, ydist + button_EXM_dist*0, button_w, button_EXM_h,    "∅", 26, button_EXM_average_pressed,   False)
button_EXM_matrix    = Menu.button(xdist, ydist + button_EXM_dist*1, button_w, button_EXM_h,    "◯", 20, button_EXM_matrix_pressed,    False)
button_EXM_spot      = Menu.button(xdist, ydist + button_EXM_dist*2, button_w, button_EXM_h,     "◯", 6, button_EXM_spot_pressed,      False)
button_EXM_backlit   = Menu.button(xdist, ydist + button_EXM_dist*3, button_w, button_EXM_h,    "☄", 20, button_EXM_backlit_pressed,   False)
button_EXP_mode      = Menu.button(xdist,  h - ydist - button_EXM_h, button_w, button_EXM_h,  "MODE", 10, button_EXP_mode_pressed,      False)
#Create buttons for EXP Mode Menu (nested)
button_EXP_auto      = Menu.button(xdist, ydist + button_EXP_dist*0, button_w, button_EXP_h,  "AUTO", 10, button_EXP_auto_pressed,      False)
button_EXP_night     = Menu.button(xdist, ydist + button_EXP_dist*1, button_w, button_EXP_h, "NIGHT", 10, button_EXP_night_pressed,     False)
button_EXP_backlight = Menu.button(xdist, ydist + button_EXP_dist*2, button_w, button_EXP_h,    "BL", 12, button_EXP_backlight_pressed, False)
button_EXP_spotlight = Menu.button(xdist, ydist + button_EXP_dist*3, button_w, button_EXP_h,    "SL", 12, button_EXP_spotlight_pressed, False)
button_EXP_sports    = Menu.button(xdist, ydist + button_EXP_dist*4, button_w, button_EXP_h, "SPORT",  8, button_EXP_sports_pressed,    False)
button_EXP_snow      = Menu.button(xdist, ydist + button_EXP_dist*5, button_w, button_EXP_h,  "SNOW",  8, button_EXP_snow_pressed,      False)
button_EXP_beach     = Menu.button(xdist, ydist + button_EXP_dist*6, button_w, button_EXP_h, "BEACH",  8, button_EXP_beach_pressed,     False)
button_EXP_fireworks = Menu.button(xdist, ydist + button_EXP_dist*7, button_w, button_EXP_h, "FWORK",  8, button_EXP_fireworks_pressed, False)
button_EXP_antishake = Menu.button(xdist, ydist + button_EXP_dist*8, button_w, button_EXP_h, "SHAKE",  8, button_EXP_antishake_pressed, False)
#Change visibility of EXP Menu
def visibility_Menu_EXP(visibility):
    if visibility:
        button_EXM_average.show()
        button_EXM_matrix.show()
        button_EXM_spot.show()
        button_EXM_backlit.show()
        button_EXP_mode.show()
        button_EXM_average.setFocus() #Set Focus
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
checkbox_ETC_FoM     = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*0, checkbox_w, checkbox_h, "FoM", 8, setting_FoM,               checkbox_ETC_FoM_pressed,     False)
checkbox_ETC_raw     = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*1, checkbox_w, checkbox_h, "RAW", 7, setting_raw,               checkbox_ETC_raw_pressed,     False)
checkbox_ETC_flicker = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*2, checkbox_w, checkbox_h, "Hz", 12, setting_flicker_init_bool, checkbox_ETC_flicker_pressed, False)
checkbox_ETC_hf      = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*3, checkbox_w, checkbox_h, "HF", 12, setting_hf,                checkbox_ETC_hf_pressed,      False)
checkbox_ETC_vf      = Menu.checkbox(xdist, ydist + checkbox_ETC_dist*4, checkbox_w, checkbox_h, "VF", 12, setting_vf,                checkbox_ETC_vf_pressed,      False)
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
button_PIC_next   = Menu.button(xdist, ydist + button_PIC_dist*0, button_w, button_PIC_h,  "►", 12, button_PIC_next_pressed,   False)
button_PIC_prev   = Menu.button(xdist, ydist + button_PIC_dist*1, button_w, button_PIC_h,  "◄", 12, button_PIC_prev_pressed,   False)
button_PIC_rotate = Menu.button(xdist, ydist + button_PIC_dist*2, button_w, button_PIC_h,  "↻", 20, button_PIC_rotate_pressed, False)
button_PIC_save   = Menu.button(xdist, ydist + button_PIC_dist*3, button_w, button_PIC_h, "✓", 20, button_PIC_save_pressed,   False)
button_PIC_BAK    = Menu.button(xdist,  h - ydist - button_PIC_h, button_w, button_PIC_h,  "↩", 24, button_PIC_BAK_pressed,    False)
#Change visibility of PIC Menu
def visibility_Menu_PIC(visibility):
    if visibility:
        button_PIC_next.show()
        button_PIC_prev.show()
        button_PIC_rotate.show()
        button_PIC_save.show()
        button_PIC_BAK.show()
        button_PIC_next.setFocus() #Set Focus
    else:
        button_PIC_next.hide()
        button_PIC_prev.hide()
        button_PIC_rotate.hide()
        button_PIC_save.hide()
        button_PIC_BAK.hide()


##Run App##────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Menu.show()
sys.exit(App.exec())
