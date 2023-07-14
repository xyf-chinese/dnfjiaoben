import cv2
import pyautogui
import numpy as np
import os
import time
import keyboard
import threading

time.sleep(3)


#匹配图片
def find_image_on_screen(image_path,screen):
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]  
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
    return max_loc, max_val, w, h


screenshot = pyautogui.screenshot()
screenshot_np = np.array(screenshot)
screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB) 
#image = 'C:\\Users\\xyf\\Desktop\\chc\\shuatu\\zero_pilao.png'
#img_pilao = screenshot_np[190:280,226:390]
pilao_img_check = screenshot_np[190:280,226:390]
image='C:\\Users\\xyf\\Desktop\\chc\\zero_pilao.png'
loc,conf,w,h=find_image_on_screen(image,pilao_img_check)
print(conf)

#0.73 退出匹配率0.7
