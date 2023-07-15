import cv2
import pyautogui
import numpy as np
import os
import time
import keyboard
import threading

screen = None
screen_lock = threading.Lock()
pyautogui.PAUSE=0.2
re_img = 'C:\\Users\\82325\\Desktop\\jiaoben\\dnfjiaoben\\chc\\shuatu\\re.png' #重新进图图片
xiuli_img = "C:\\Users\\82325\\Desktop\\jiaoben\\dnfjiaoben\\chc\\xiuli.png"

#截取屏幕
def load_screen():
    global screen
    while True:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)     
        with screen_lock:
            screen = screenshot_np   
        time.sleep(0.5)  

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

#普通角色刷图
def nattack():
        pyautogui.moveTo(1600,826)
        pyautogui.mouseDown()
        time.sleep(3.5)  
        pyautogui.mouseUp()   
        pyautogui.click(1285,869)
        time.sleep(0.2)
        pyautogui.moveTo(1600,826)
        pyautogui.mouseDown()
        time.sleep(3.2)  
        pyautogui.mouseUp()   
        pyautogui.click(1285,869)
        time.sleep(0.12)
        pyautogui.click(1160,870)

#风土刷图
def sattack():
    pyautogui.moveTo(1525,737)
    pyautogui.mouseDown()
    time.sleep(3)  
    pyautogui.mouseUp()

#装备修理  
def zhuangebixiuli():
    zhuangbeixiuli_image='C:\\Users\\82325\\Desktop\\jiaoben\\dnfjiaoben\\chc\\zhuangbeixiuli.png'
    loc,conf,w,h=find_image_on_screen(zhuangbeixiuli_image,screen)  
    if conf >0.75: #修理
       time.sleep(1)
       click_img(loc,conf,w,h)
       pyautogui.click(1424,844) #修理
       time.sleep(1)
       pyautogui.click(1568,229) #x
       time.sleep(1)

#图中修理
def tu_xiuli(): 
    global xiuli_img
    loc, conf, w, h = find_image_on_screen(xiuli_img,screen)
    if conf > 0.7:            
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
     time.sleep(1)

#重新进图 
def re_in():
    global re_img
    loc,conf,w,h=find_image_on_screen(re_img,screen)
    if conf> 0.75:
         zhuangebixiuli() #修装备
         tu_xiuli()   #清背包
         #fanhui_flg =fanhui()
         #if fanhui_flg == 1:
            #return 0
         click_img(loc,conf,w,h)     
         time.sleep(1)
         pyautogui.click(1056,637)
         time.sleep(2)
         return 1
    
#空疲劳换角色
def fanhui():
    time.sleep(1)
    fanhui_path = 'C:\\Users\\82325\\Desktop\\jiaoben\\dnfjiaoben\\chc\\fanhui.png'
    loc,conf,w,h=find_image_on_screen(fanhui_path,screen)
    if conf>0.7:
        click_img(loc,conf,w,h)
        time.sleep(6)
        pyautogui.click(1705,185) #点击菜单
        time.sleep(1)
        pyautogui.click(1587,880) #选择角色
        time.sleep(12)
        return 1 # 1 空疲劳
#按下esc退出
def check_exit():
     while True:
        if keyboard.is_pressed('esc'):
            os._exit(0)
        time.sleep(0.1)          

if __name__ == "__main__":
   time.sleep(1)
   screen_thread = threading.Thread(target=load_screen, daemon=True)
   screen_thread.start()
   #按下esc暂停脚本 
   exit_thread = threading.Thread(target=check_exit, daemon=True)
   exit_thread.start()
   time.sleep(2)
   chc_type = 1   #1普通角色 0风土角色
   while True:
        if chc_type == 1:
           nattack()     
        else:
           sattack()
        re_in_flg = re_in()   
        if re_in_flg ==0:
           break
                        
        
