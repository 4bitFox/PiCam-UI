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
  - Font size
- Default settings
- Hardware integration:
  - GPIO Pins
    - Shutter button
    - Navigation buttons
  - Code for Battery level
  - Code for RTC

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
