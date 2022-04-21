import keyboard
import win32api
import win32con
from pyautogui import *

from checkPicExits import check_pic_exist

target_region = (753, 153, 1166, 886)

dictionary_name = 'meituan_imgs'
# dictionary_name = 'dingdong_imgs'
pic_list = os.listdir(dictionary_name)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def check_keyboard():
    if keyboard.is_pressed('q'):
        return False
    if keyboard.is_pressed('enter'):
        return False
    return True


def auto_supplement_inventory(pic_result_list):
    print('购物车已空,开始自动寻找库存')
    cur_pic_info = [x[1] for x in pic_result_list if 'index' in x[0]][0]
    click(cur_pic_info[0], cur_pic_info[1])  # 最后1张图的坐标


if __name__ == '__main__':
    s = '2022-04-21 05:50:00'
    while True:
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        if current_time < s:
            print("时间未到 休息5分钟", current_time)
            time.sleep(300)
        else:
            print('开始自动抢菜抢菜', current_time)
            break

    while check_keyboard():
        pic_result_list = []
        for pic in pic_list:
            result = check_pic_exist(pic_name=pic, confidence=0.8,
                                     dictionary_name=dictionary_name)  # confidence 为图片识别的速度 调低会导致识别不到
            if result:
                pic_result_list.append((pic, result))

        if len(pic_result_list) > 0:
            print(pic_result_list)
            # 获取到成功的图片文案
            if 'final' in ','.join([x[0] for x in pic_result_list]):
                print('抢单成功!')
                file_name = 'sing.mp3'
                os.system(file_name)
                break
            elif 'full' in ','.join([x[0] for x in pic_result_list]):
                print('今日约满!刷可新派送时间!')
                cur_pic_info = [x[1] for x in pic_result_list if '0-back' in x[0]][0]
                click(cur_pic_info[0], cur_pic_info[1])  # 最后1张图的坐标

            elif 'timeslot' in ','.join([x[0] for x in pic_result_list]):
                cur_pic_info = [x[1] for x in pic_result_list if 'timeslot' in x[0]][0]
                click(cur_pic_info[0], cur_pic_info[1])  # 最后1张图的坐标
                click(cur_pic_info[0], cur_pic_info[1] + 55)
                # sleep(0.3)
                # sleep(0.3)
                click(cur_pic_info[0], cur_pic_info[1] + 110)
                # sleep(0.3)
                click(cur_pic_info[0], cur_pic_info[1] + 160)
                # sleep(0.3)
            else:
                cur_pic_info = [x[1] for x in pic_result_list if
                                int(x[0].split('-')[0]) == max([int(y[0].split('-')[0]) for y in pic_result_list])][0]
                click(cur_pic_info[0], cur_pic_info[1])
                sleep(0.1)
        else:
            print('无法获取到对应图片')
            time.sleep(1)
