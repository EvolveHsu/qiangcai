import operator
import time

import keyboard
import win32api
import win32con
from pyautogui import *

from checkPicExits import check_pic_exist

dictionary_name = 'meituan_imgs'
pic_list = os.listdir(dictionary_name)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def check_stop_keyboard():
    if keyboard.is_pressed('q'):
        return False
    if keyboard.is_pressed('enter'):
        return False
    return True


if __name__ == '__main__':
    s = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d 05:50:00')
    print('设定开始时间: ', s)
    while True:
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        if current_time < s:
            print("时间未到 休息5分钟", current_time)
            time.sleep(300)
        else:
            print('开始自动抢菜抢菜', current_time)
            break

    while check_stop_keyboard():
        pic_obj_list = []
        for pic in pic_list:
            result = check_pic_exist(pic_name=pic, confidence=0.8,
                                     dictionary_name=dictionary_name)  # confidence 为图片识别的速度 调低会导致识别不到
            if result:
                spl_pic = pic.split('-')
                num = spl_pic[0]
                pic_name = spl_pic[1].split('.')[0]
                pic_obj_list.append({
                    'num': int(num),
                    'pic_name': pic_name,
                    'x_index': result[0],
                    'y_index': result[1],
                })

        if len(pic_obj_list) > 0:
            print(pic_obj_list)
            pic_obj_list = sorted(pic_obj_list, key=operator.itemgetter('num'), reverse=True)
            # 获取到成功的图片文案
            img_append_str = ','.join([x.get('pic_name') for x in pic_obj_list])
            if 'final' in img_append_str:
                print('抢单成功!')
                file_name = 'sing.mp3'
                os.system(file_name)
                break
            else:
                cur_pic_info = pic_obj_list[0]
                print(cur_pic_info)
                click(cur_pic_info.get('x_index'), cur_pic_info.get('y_index'))
                sleep(0.5)  # 这里识别过快会导致不停的全选
        else:
            print('无法获取到对应图片')
            time.sleep(1)
