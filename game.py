import cv2
import pyautogui
import numpy as np
import os
import time

def find_image_on_screen(image_path):
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]  # 添加这一行获取模板图片的宽度和高度
    res = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc, max_val, w, h  

def click_on_location(location, confidence, w, h):  # 修改这一行以接收宽度和高度
    if confidence > 0.8:
        pyautogui.click(location[0] + w // 2, location[1] + h // 2)
        return True
    return False

if __name__ == "__main__":
    folder_path = "C:\\Users\\xyf\\Desktop\\1"  # 文件夹路径
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]
    print("开始匹配图片并执行点击...")
#--------------------------------------------------------------------------------------------------------------
    while True:
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            loc, conf, w, h = find_image_on_screen(img_path)  # 修改这一行以接收宽度和高度
            if click_on_location(loc, conf, w, h):  # 修改这一行以传递宽度和高度
                print(f"在屏幕上找到了图片 {img}，已点击")
            time.sleep(1)
