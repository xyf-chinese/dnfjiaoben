import cv2
import pyautogui
import numpy as np
import os
import time
import keyboard
import threading
from datetime import datetime

time.sleep(2)
pilao0 = '.\\chc\\pilao0.png'
pyautogui.PAUSE=0.2
shuatu_path = ".\\chc\\shuatu" 
shuatu_files = [f for f in os.listdir(shuatu_path) if f.endswith('.png') or f.endswith('.jpg')]
pilaofuzu_flg=0
shenyuan_flg = 0 #1深渊

screen = None
screen_lock = threading.Lock()
stuck = 0
stuck_lock = threading.Lock()

#按下esc退出
def check_exit():
     while True:
        if keyboard.is_pressed('esc'):
            os._exit(0)
        time.sleep(0.1)

#卡住移动操作
def whilestuck():
   time.sleep(10)
   global stuck 
   stuckrepair_img = ('.\\chc\\stuck.png')
   max_time = 30
   while True:
      loc,conf,w,h =  find_image_on_screen(stuckrepair_img,screen)
      if conf > 0.7:
         with stuck_lock:
            stuck +=1
            if stuck > 30:
               pyautogui.click(291,723)
               time.sleep(1)
               pyautogui.click(291,723)
               stuck  = 0
      time.sleep(1)           
           
#截取屏幕
def load_screen():
    global pilaofuzu_flg
    global screen
    global shenyuan_flg
    while True:
        now = datetime.now()
        if now.hour == 5:
         time.sleep(5)
         os.system('D:/bianchengruanjian/ADB/platform-tools/adb shell input keyevent 26')   
         time.sleep(300)
         os.system('shutdown /s /t 1') 
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)     
        with screen_lock:
            screen = screenshot_np   
        pilaobuzu_img= '.\\chc\\pilaobuzu.png'
        shenyuan_flg_img = '.\\chc\\shenyuan.png'
        loc,conf,w,h=find_image_on_screen(pilaobuzu_img,screen)
        if conf>0.8:
           pilaofuzu_flg =1
        loc,shenyuan_conf,w,h = find_image_on_screen(shenyuan_flg_img,screen)
        if shenyuan_conf>0.7:
           shenyuan_flg =1  
        time.sleep(0.2)        
                      

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
        
#疲劳检查 0空疲劳 1有疲劳
def pilao0_check():
    with screen_lock:     
     pilao_img_check = screen[193:299,222:397]
    loc,conf,w,h = find_image_on_screen(pilao0,pilao_img_check)
    time.sleep(1)
    if conf>=0.91:
       return 0
    elif conf<0.91:
       return 1
   
#返回主界面   
def re_main():       
    pyautogui.click(1703,187)   
    time.sleep(2)
    pyautogui.click(1590,885)
    time.sleep(10)
    
#角色自动修理装备,清空背包       
def xiuli():
    pyautogui.click(1702,887) #背包
    time.sleep(2)
    pyautogui.click(1700,900) #分解
    time.sleep(2)
    pyautogui.click(1426,843) #分解界面中分解
    time.sleep(2)
    pyautogui.click(1082,738) # 确认
    time.sleep(2) 
    pyautogui.click(964,644)  #确认
    time.sleep(2)
    pyautogui.click(1574,228) #返回
    time.sleep(2)
    pyautogui.click(1601,892) #出售
    time.sleep(2)
    pyautogui.click(1419,847) #出售界面中出售
    time.sleep(2)
    pyautogui.click(1076,670) #确认
    time.sleep(2)
    pyautogui.click(964,644) #确认
    time.sleep(2)
    pyautogui.click(1574,228) #返回
    time.sleep(2)
    pyautogui.click(1085,906) #修理图标
    time.sleep(2)
    pyautogui.click(1422,843) #修理
    time.sleep(2)
    pyautogui.click(1570,234) #返回
    time.sleep(2)
    pyautogui.click(195,169) #背包返回
    time.sleep(2)
    
#自动进图
def dugeon_in():
    pyautogui.moveTo(383,809)
    pyautogui.mouseDown()
    time.sleep(0.8)
    pyautogui.mouseUp()
    time.sleep(3)
    pyautogui.moveTo(291,723)
    pyautogui.mouseDown()
    time.sleep(4)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.mouseDown()
    time.sleep(9)
    pyautogui.mouseUp()


#进图检测，进入山脊
def shanji_in():
    shanji_in_img = '.\\chc\\shanji_in.png'    
    loc,conf,w,h =find_image_on_screen(shanji_in_img,screen)
    if conf>0.8 :
       pyautogui.click(294,359)#冒险级
       time.sleep(2)
       pyautogui.click(699,682) #山脊
       time.sleep(2)
       pyautogui.click(1438,817) #战斗开始
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
    time.sleep(3.5)  
    pyautogui.mouseUp()

#再次挑战    
def re_in(img_path,cha_type):
    global stuck
    zhuangebixiuli() #修装备
    zero_pilao_path ='.\\chc\\zero_pilao.png' 
    kong_screen = screen[190:280,226:390]
    loc,conf,w,h=find_image_on_screen(zero_pilao_path,kong_screen) #0疲劳回城
    if conf>0.7: 
       return 1 
    tu_xiuli_path = '.\\chc\\xiuli.png' #清背包
    loc,conf,w,h=find_image_on_screen(tu_xiuli_path,screen)
    if conf > 0.7:
        tu_xiuli(tu_xiuli_path)      
    loc, conf, w, h = find_image_on_screen(img_path,screen) #下一把
    if conf > 0.65:          
     if cha_type ==1 :
        sattack()
     if cha_type == 0:
        time.sleep(0.12)
        pyautogui.moveTo(1600,826)
        pyautogui.mouseDown()
        time.sleep(2.9)  
        pyautogui.mouseUp()                
     click_img(loc,conf,w,h)
     with stuck_lock:
      stuck  = 0 
     time.sleep(1)
     pyautogui.click(1056,637)
     time.sleep(2)
     return 0   
    return 0 

#装备修理  
def zhuangebixiuli():
    zhuangbeixiuli_image='.\\chc\\zhuangbeixiuli.png'
    loc,conf,w,h=find_image_on_screen(zhuangbeixiuli_image,screen)  
    if conf >0.75: #修理
       time.sleep(1)
       click_img(loc,conf,w,h)
       pyautogui.click(1424,844) #修理
       time.sleep(1)
       pyautogui.click(1568,229) #x
       time.sleep(1)
          
#图中修理
def tu_xiuli(img_path): 
    loc, conf, w, h = find_image_on_screen(img_path,screen)
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
     
#空疲劳换角色
def fanhui():
    time.sleep(1)
    fanhui_path = '.\\chc\\fanhui.png'
    loc,conf,w,h=find_image_on_screen(fanhui_path,screen)
    if conf>0.7:
        click_img(loc,conf,w,h)
        time.sleep(6)
        pyautogui.click(1705,185) #点击菜单
        time.sleep(1)
        pyautogui.click(1587,880) #选择角色
        time.sleep(12)
        return 1
    
def pilaobuzu():  #深渊刷完回城
      pyautogui.click(1705,185) #点击菜单
      time.sleep(1)
      pyautogui.click(1587,880) #选择角色
      time.sleep(10)
         
      
                         
#遇到深渊回城
def shenyuanfanhui():
    time.sleep(2)
    pyautogui.click(1551,172) #设置
    time.sleep(2)
    pyautogui.click(1441,871) #返回城镇
    time.sleep(1)
    pyautogui.click(1060,648) #确认
    time.sleep(6)
    pilao000 = '.\\chc\\pilao0.png'
    pilao_img_check = screen[190:280,226:390]
    loc,conf,w,h = find_image_on_screen(pilao000,pilao_img_check)
    print(conf)
    if conf > 0.85:
       return 1  
    else:   
      pyautogui.moveTo(301,728) #摇杆左
      pyautogui.mouseDown()
      time.sleep(1)
      pyautogui.mouseUp()
      time.sleep(1)
      shanji_in()
      return 0
    
                                       

#角色1刷图 65土
def t1controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t1.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()   
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                      
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          print('角色1完成 最后一把非深渊')
                          return

                              
                   
#角色2刷图 55土            
def t2controll(cha_type):
       global shenyuan_flg
       global pilaofuzu_flg
       chc_path = '.\\chc\\t2.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue            
                 if img_name == 're':           
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                      
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          print('角色2完成')
                          return
                                  

#角色3刷图 55土            
def t3controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t3.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue          
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                      
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

                   
#角色4刷图 55土            
def t4controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t4.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue            
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return


#角色5刷图 55土            
def t5controll(cha_type):
       global pilaofuzu_flg 
       global shenyuan_flg
       chc_path = '.\\chc\\t5.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue             
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                      
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

#角色6刷图 n           
def t6controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t6.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

#角色7刷图 n           
def t7controll(cha_type):
       global shenyuan_flg
       global pilaofuzu_flg
       chc_path = '.\\chc\\t7.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                     
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return
#角色8刷图 n           
def t8controll(cha_type):
       global shenyuan_flg
       global pilaofuzu_flg
       chc_path = '.\\chc\\t8.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                     
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                    
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return   

#角色9刷图 n           
def t9controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t9.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                       sattack()
                    elif cha_type==0:
                       nattack()                     
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return                                                                                                               
                                                     
#角色10刷图 n           
def t10controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t10.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                   
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return      
#角色11刷图 n           
def t11controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t11.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                    
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return   
#角色12刷图 n           
def t12controll(cha_type):
       global pilaofuzu_flg
       global shenyuan_flg
       chc_path = '.\\chc\\t12.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return  

#角色13刷图 n           
def t13controll(cha_type):
       global shenyuan_flg 
       global pilaofuzu_flg
       chc_path = '.\\chc\\t13.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

#角色14刷图 n           
def t14controll(cha_type):
       global shenyuan_flg 
       global pilaofuzu_flg
       chc_path = '.\\chc\\t14.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

#角色15刷图 n           
def t15controll(cha_type):
       global shenyuan_flg 
       global pilaofuzu_flg
       chc_path = '.\\chc\\t15.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                   
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return

#角色16刷图 n           
def t16controll(cha_type):
       global shenyuan_flg 
       global pilaofuzu_flg
       chc_path = '.\\chc\\t16.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                   
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return     

#角色17刷图 n           
def t17controll(cha_type):
       global shenyuan_flg 
       global pilaofuzu_flg
       chc_path = '.\\chc\\t17.png'
       loc,conf,w,h=find_image_on_screen(chc_path,screen)
       if conf>0.85:   
        click_img(loc,conf,w,h)
        time.sleep(1)
        click_img(loc,conf,w,h)   
        pyautogui.click(945,900)
        time.sleep(1)
        pyautogui.click(945,900)
        time.sleep(15)
        pilao_flg = pilao0_check()
        if pilao_flg == 0:
            re_main()            
        elif pilao_flg ==1 :
            xiuli() 
            dugeon_in()
            shanji_in()
            while True:
             for img in shuatu_files:
                 img_name,img_ext = os.path.splitext(img)
                 img_path = os.path.join(shuatu_path, img)
                 if shenyuan_flg ==1:
                    shenyuanfanhuires = shenyuanfanhui()#遇到深渊返回
                    if shenyuanfanhuires == 1:
                       time.sleep(5)
                       shenyuan_flg = 0
                       pilaobuzu()
                       time.sleep(10)
                       break
                    else:    
                       pass
                    shenyuan_flg =0
                    continue                   
                 if img_name == 're':                    
                    fanhui_flg = re_in(img_path,cha_type) #0为有疲劳 1为空疲劳返回
                    if cha_type==1: #选择攻击模式
                     sattack()
                    elif cha_type==0:
                     nattack()                       
                    if fanhui_flg ==1:
                       fanhui_res = fanhui()
                       if fanhui_res==1:
                          return                                                                             
                                                                                                               
                                                         
if __name__ == "__main__": 
   #按下esc暂停脚本 
   exit_thread = threading.Thread(target=check_exit, daemon=True)
   exit_thread.start()
    
   screen_thread = threading.Thread(target=load_screen, daemon=True)
   screen_thread.start()
   
   stuckrepair_thread = threading.Thread(target=whilestuck,daemon=True)
   stuckrepair_thread.start()
   
   
   time.sleep(2)
   #从第几个角色开始刷，调节 1 开始
   chc_n = 1
   cha_type = 0 #角色类型 0普通 1风土
   if chc_n == 1: #角色1
      print('角色1启动')
      cha_type=1
      t1controll(cha_type)
      chc_n += 1
      print(chc_n)
   
   if chc_n ==2: #角色2
      print('角色2启动')
      cha_type=1 
      t2controll(cha_type)
      chc_n += 1  
      print(chc_n) 
   
   if chc_n ==3: #角色3
      cha_type=1    
      t3controll(cha_type)
      chc_n += 1   
   
   if chc_n ==4: #角色4
      cha_type=1    
      t4controll(cha_type)
      chc_n += 1   

   if chc_n ==5: #角色5
      cha_type=1    
      t5controll(cha_type)
      chc_n += 1
   
   if chc_n ==6: #角色6
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t6controll(cha_type)
      chc_n += 1  
            
   if chc_n ==7: #角色7
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t7controll(cha_type)
      chc_n += 1   
      
   if chc_n ==8: #角色8
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t8controll(cha_type)
      chc_n += 1    
                    
   if chc_n ==9: #角色9
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t9controll(cha_type)
      chc_n += 1    

   if chc_n ==10: #角色10
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t10controll(cha_type)
      chc_n += 1                         
   
   if chc_n ==11: #角色11
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t11controll(cha_type)
      chc_n += 1      
   
   if chc_n ==12: #角色12
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t12controll(cha_type)
      chc_n += 1    

   if chc_n ==13: #角色13
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t13controll(cha_type)
      chc_n += 1   
 
   if chc_n ==14: #角色14
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t14controll(cha_type)
      chc_n += 1    
      
   if chc_n ==15: #角色15
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      cha_type=0    
      t15controll(cha_type)
      chc_n += 1  

   if chc_n ==16: #角色16
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      pyautogui.scroll(-1) 
      time.sleep(5)      
      cha_type=0    
      t16controll(cha_type)
      chc_n += 1  

   if chc_n ==17: #角色17
      pyautogui.moveTo(960,550) #鼠标回到中央
      time.sleep(1)
      pyautogui.scroll(-1) 
      time.sleep(5)        
      pyautogui.scroll(-1) 
      time.sleep(5)
      pyautogui.scroll(-1) 
      time.sleep(5)      
      cha_type=0    
      t17controll(cha_type)
      chc_n += 1      
             
   time.sleep(5)
   os.system('D:/bianchengruanjian/ADB/platform-tools/adb shell input keyevent 26')   
   time.sleep(300)
   os.system('shutdown /s /t 1')  

                     
   
   
   
    
   

