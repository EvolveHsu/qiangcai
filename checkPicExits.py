#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:Evolve Hsu
@file:checkPicExits.py
@time:2022/04/05
"""

import os
import pyautogui


def check_pic_exist(pic_name, confidence, dictionary_name):
    abs_path = os.getcwd()  # 获取当前项目绝对路径
    pic_path = os.path.join(abs_path, dictionary_name, pic_name)
    result = pyautogui.locateCenterOnScreen(pic_path, confidence=confidence, grayscale=True)
    return result
