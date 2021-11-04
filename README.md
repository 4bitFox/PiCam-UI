# PiCam - UI for portable Raspberry Pi Camera

### SCRIPT IS FUNCTIONAL BUT NOT FINISHED YET!

This Script makes a basic UI for controlling and viewing Camera settings.
![IMG_20210509_153426](https://user-images.githubusercontent.com/33175205/117574342-f5ea5180-b0dc-11eb-8474-cdfd6e015b4d.jpg)
Images can be viewed with feh.
![Screenshot_20210509_153545](https://user-images.githubusercontent.com/33175205/117574195-3b5a4f00-b0dc-11eb-8b8f-6437dac5f8ea.png)

It is verry likely that you'll have to make changes in the code to make it work for your hardware and needs.
For example:
- Screen and Preview resolution
```py
wscreen  = 800 #Screen width
hscreen  = 480 #Screen height
wpreview = 640 #Preview width (https://andrew.hedges.name/experiments/aspect_ratio/)
wmenu    = 100 #Menu with (left)
```
  - Font size (adjust if you changed some of the above)
```py
#                                                                               Font size
#                                                                                  ▼▼
button_ISO = Menu.button(xdistl, ydist + button_dist*0, button_w, button_h, "ISO", 26, button_ISO_pressed, True)
button_SS  = Menu.button(xdistl, ydist + button_dist*1, button_w, button_h,  "SS", 26,  button_SS_pressed, True)
button_AWB = Menu.button(xdistl, ydist + button_dist*2, button_w, button_h, "AWB", 26, button_AWB_pressed, True)
button_EXP = Menu.button(xdistl, ydist + button_dist*3, button_w, button_h, "EXP", 26, button_EXP_pressed, True)
button_ETC = Menu.button(xdistl,  h - ydist - button_h, button_w, button_h,   "⚙", 30, button_ETC_pressed, True)
```
- Default settings
```py
#Output settings
setting_output_location = "/home/pi/Pictures" #Where to store pictures
setting_output_prefix = "FCM_"   #Filename prefix
setting_output_suffix_noraw = "" #Filename suffix when RAW disabled
setting_output_suffix_raw = "R"  #Filename suffix when RAW enabled
setting_encoding = "jpg"         #Encoding of picture taken
setting_mode = 3                 #Sensor mode
setting_quality = 90             #Compression quality
setting_thumbnail = "64,48,35" #Thumbnail settings ("width,height,quality")


#Default Camera settings
setting_ISO = 0        #ISO
setting_AWB = "auto"   #Auto White Balance
setting_SS  = 0        #Shutter Speed
setting_EXP = "auto"   #Exposure Mode
setting_EXM = "matrix" #Exposure Metering
#Default additional settings
setting_FoM     = False  #Display focus FoM value
setting_raw     = False  #Add raw Bayer data to JPEG
setting_flicker = "50hz" #Flicker avoidance
setting_hf      = False  #Flip Image horizontally
setting_vf      = False  #Flip Image vertically
#Default advanced settings
setting_USB  = True
setting_HDMI = True
setting_WiFi = True
setting_SSH  = True
setting_VNC  = True

#Artist
setting_photographer = "YOUR NAME HERE" #Name of photographer (for EXIF Artist)





#Other
title = "PiCam"
cursor_hidden = True
style = "line-keys" #How the UI looks. You can use "boxes", "line", "line-keys" or "line-touch"
debugging = False #Debugging (print stuff to console)
```
- Hardware integration:
  - GPIO Pins
```py
#GPIO Buttons
#If you use buttons connected to GPIO, you can set the pin numbers here:
button_capture = Button(5) #Take a photo
button_up      = Button(13) #Move up in menu
button_select  = Button(26) #Select in menu
button_down    = Button(19) #Move down in menu
```
  - Battery and RTC
```py
#Hardware
hw_battery = False #Enable battery. You have change the "battery()" function yourself if you use something different than a pisugar: https://github.com/PiSugar/PiSugar/wiki/PiSugar-Power-Manager-(Software)
hw_utc = False #Enable UTC. You have change the "utc()" function yourself if you use something different than a pisugar: https://github.com/PiSugar/PiSugar/wiki/PiSugar-Power-Manager-(Software)
```

Script:
https://raw.githubusercontent.com/4bitFox/PiCam-UI/main/PiCam/PiCam.py

### Hardware I personally use:
- Raspberry Pi 4 Model B: https://www.raspberrypi.org/products/raspberry-pi-4-model-b/
- Raspberry Pi HQ Camera: https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/
- Waveshare 4.3" DSI LCD: https://www.waveshare.com/4.3inch-DSI-LCD.htm
- PiSugar 2 Pro: https://www.tindie.com/products/pisugar/pisugar2-pro-battery-for-raspberry-pi-3b3b4b/

And of course:
- C & CS Mount lenses
- Some generic push-buttons
- A case thet I 3D printed
  - Screws & Glue
