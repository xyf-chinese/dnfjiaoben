import cv2
import pyautogui
import numpy as np
import os
import time
import keyboard
import threading

time.sleep(3)
image_path = "C:\\Users\\xyf\\Desktop\\ddnnff" 
image_files = [f for f in os.listdir(image_path) if f.endswith('.png') or f.endswith('.jpg')]
pyautogui.PAUSE=0.1


def nattack():
        pyautogui.click(1285,869)
        pyautogui.moveTo(1600,826)
        pyautogui.mouseDown()
        time.sleep(3.5)  
        pyautogui.mouseUp()  
        pyautogui.click(1285,869)
        pyautogui.moveTo(1600,826)
        pyautogui.mouseDown()
        time.sleep(3.3)  
        pyautogui.mouseUp()  
        pyautogui.click(1285,869)
        time.sleep(0.3)
        pyautogui.click(1160,870)
def sattack():
        pyautogui.moveTo(1525,737)
        pyautogui.mouseDown()
        time.sleep(3.5)  
        pyautogui.mouseUp()              

#匹配图片
def find_image_on_screen(image_path):
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]  
    res = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
    return max_loc, max_val, w, h

#点击图片
def click_img(location, confidence, w, h):
        pyautogui.moveTo(location[0] + w // 2, location[1] + h // 2)  
        pyautogui.click(location[0] + w // 2, location[1] + h // 2) 

#再次挑战
def reconfirm(img_path):
    xiuli_path = 'C:\\Users\\xyf\\Desktop\\ddnnff\\xiuli.png'
    loc,conf,w,h=find_image_on_screen(xiuli_path)
    if conf > 0.6:
        xiuli(xiuli_path)
    loc, conf, w, h = find_image_on_screen(img_path)  
    if conf > 0.5:         
     click_img(loc,conf,w,h)
     time.sleep(0.5)
     pyautogui.click(1056,637)

#清空背包，修理装备
def xiuli(img_path):     
    loc, conf, w, h = find_image_on_screen(img_path)
    if conf > 0.6:            
     click_img(loc,conf,w,h)
     time.sleep(2)
     pyautogui.click(1425,833)
     time.sleep(2)
     pyautogui.click(1078,742)
     time.sleep(2)
     pyautogui.click(970,642)
     time.sleep(2)
     pyautogui.click(1572,231)
     time.sleep(2)
     pyautogui.click(1596,900)
     time.sleep(2)
     pyautogui.click(1440,840)   
     time.sleep(2)
     pyautogui.click(1082,674)
     time.sleep(2)
     pyautogui.click(957,646)
     time.sleep(2)
     pyautogui.click(1570,226)
     time.sleep(2)
     pyautogui.click(1077,907)
     time.sleep(2)
     pyautogui.click(1430,826)
     time.sleep(2)
     pyautogui.click(1574,227)
     time.sleep(2)
     pyautogui.click(195,168)
     time.sleep(2)

def check_exit():
     while True:
        if keyboard.is_pressed('esc'):
            os._exit(0)
        time.sleep(0.1)     
     
if __name__ == "__main__":
   #按下esc键暂停脚本 
   exit_thread = threading.Thread(target=check_exit,daemon=True)
   exit_thread.start() 
                 
   role = 1 # 1普通 2风土
   while True:  
     for img in image_files:
        img_name,img_ext = os.path.splitext(img)
        img_path = os.path.join(image_path, img)
        #while True:
        if img_name =='xiuli': #修理装备 清空背包
            xiuli(img_path)
        if img_name == 're' : #再次挑战
            reconfirm(img_path)
        if role == 1 :    
         nattack()
        elif role == 2:
         sattack()   
             
        #if img_name =='shenyuan' 遇到深渊重新挑战