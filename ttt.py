import cv2
import pyautogui
import time
import numpy as np

def is_image_on_screen(image_path, threshold=0.8):
    # 截取屏幕
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 读取目标图像
    target_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # 在截图上搜索目标图像
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)

    # 如果目标图像在截图上，则返回True
    return (result >= threshold).any()

def main():
    image_path = '1.png'  # 要搜索的图像
    max_time = 30  # 最大时间（秒）
    start_time = time.time()

    while True:
        if is_image_on_screen(image_path):
            # 如果图像在屏幕上超过30秒，则打印消息
            if time.time() - start_time >= max_time:
                print('超过30秒')
                break
        else:
            # 如果图像不在屏幕上，则重置计时器
            start_time = time.time()

        # 每秒检查一次
        time.sleep(1)

if __name__ == '__main__':
    main()
