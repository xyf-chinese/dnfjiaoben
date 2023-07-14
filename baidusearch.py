import numpy as np
import cv2
import pyautogui 
import time
import os

time.sleep(3)

baidusearch = "C:\\Users\\xyf\\Desktop\\baidusearch" 
image_files = [f for f in os.listdir(baidusearch) if f.endswith('.png') or f.endswith('.jpg')]
pyautogui.PAUSE=0.2

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

#双击图片
def click_img(location, confidence, w, h):
    if confidence > 0.85:
        pyautogui.moveTo(location[0] + w // 2, location[1] + h // 2,duration=2)  
        pyautogui.doubleClick(location[0] + w // 2, location[1] + h // 2) 

while True:
    for img in image_files:
        img_name,img_ext = os.path.splitext(img)
        img_path = os.path.join(baidusearch, img)
        if img_name == 'chrome': #打开浏览器
          loc, conf, w, h = find_image_on_screen(img_path)
          if conf>0.85:
            print(f"在屏幕上找到了chrome，鼠标移动至chrome位置")        
            click_img(loc, conf, w, h)
            print(f"在屏幕上找到了chrome，已点击")
            time.sleep(1)
          else:
             continue 
        if img_name=='2': #搜索www.baidu.com
           loc, conf, w, h = find_image_on_screen(img_path)
           if conf>0.9:  
              print(f"在屏幕上找到了chrome搜索栏")
              pyautogui.typewrite('www.baidu.com')
              pyautogui.press('enter') 
              pyautogui.press('enter')   
           else:
              continue   