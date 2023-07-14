import cv2
import pyautogui
import numpy as np
import os
import time
import keyboard
import threading
from datetime import datetime

#匹配图片
def find_image_on_screen(image_path,screen):
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]  
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
    return max_loc, max_val, w, h

#点击图片
def click_img(location, confidence, w, h):
        pyautogui.moveTo(location[0] + w // 2, location[1] + h // 2)  
        pyautogui.click(location[0] + w // 2, location[1] + h // 2)
        time.sleep(1)
        
        
time.sleep(3)
pyautogui.moveTo(383,809)
pyautogui.mouseDown()
time.sleep(0.8)
pyautogui.mouseUp()
time.sleep(3)
while True:
    pyautogui.moveTo(470,724)
    pyautogui.mouseDown()
    time.sleep(1)
    pyautogui.mouseUp()
    jiuguanditu_img = '.\\chc\\jiuguan.png'  
    loc,conf,w,h =find_image_on_screen(jiuguanditu_img,screen)
    if conf>0.8 : 
        click_img(loc,conf,w,h)
        time.sleep(5)
        pyautogui.moveTo(470,724)
        pyautogui.mouseDown()
        time.sleep(8)
        pyautogui.mouseUp()
    time.sleep(0.2)    
            

#进图检测，进入酒馆
def jiuguan_in():
       pyautogui.click(860,550) #山脊
       time.sleep(2)
       pyautogui.click(1420,800) #战斗开始
       time.sleep(1)        