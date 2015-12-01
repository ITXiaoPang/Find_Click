# -*- coding: utf-8 -*-

__author__ = 'ITXiaoPang'

import ctypes
import logging
import logging.config
import logging.handlers
import os
import platform
import random
import time

import autopy
import autopy.bitmap
import autopy.mouse

# Config
my_Hide_In_Taskbar = False
my_tolerance = 0.0
my_scan_frequency = 2
my_delay_move_min = 0
my_delay_move_max = 0
my_delay_click_min = 0
my_delay_click_max = 1

# Path
my_directory = os.path.split(os.path.realpath(__file__))[0]
my_file_name = os.path.basename(__file__)
my_file_name_without_ext = os.path.splitext(my_file_name)[0]

my_images_directory_name = r'images'
my_logs_directory_name = r'logs'
my_config_directory_name = r'config'
my_config_file_name = '.'.join([my_file_name_without_ext, u'ini'])

merge_path = lambda x: os.sep.join([my_directory, x])
my_images_directory_path = merge_path(my_images_directory_name)
my_logs_directory_path = merge_path(my_logs_directory_name)
my_config_directory_path = merge_path(my_config_directory_name)
my_config_directory_full_path = os.sep.join([my_config_directory_path, my_config_file_name])
# Logging
logging.config.fileConfig(my_config_directory_full_path)
logger = logging.getLogger(os.path.basename(__file__))


def try_hide_me():
    if platform.system() in 'Windows' and my_Hide_In_Taskbar:
        my_ConsoleWindow = ctypes.windll.kernel32.GetConsoleWindow()
        if my_ConsoleWindow != 0:
            ctypes.windll.user32.ShowWindow(my_ConsoleWindow, 0)
            ctypes.windll.kernel32.CloseHandle(my_ConsoleWindow)


def sleep_random_time(min_time=1, max_time=10):
    my_random_time = random.uniform(min_time, max_time)
    logger.info(str(my_random_time).join(['Sleep: ', ' seconds']))
    time.sleep(my_random_time)


def generate_image_list(my_images_directory_path):
    if os.path.exists(my_images_directory_path):
        my_image_files_name_list = os.listdir(my_images_directory_path)
    else:
        my_image_files_name_list = None
    return my_image_files_name_list


def find_image_location_in_screen(my_image):
    my_screen = autopy.bitmap.capture_screen()
    my_rect = my_screen.find_bitmap(my_image, my_tolerance)
    if my_rect:
        my_rect = list(my_rect)
        my_rect[0] += my_image.width / 2
        my_rect[1] += my_image.height / 2
        my_rect = tuple(my_rect)
    return my_rect


def do_simulation(my_images):
    can_find = False
    my_index = -1
    for my_image in my_images:
        my_index += 1
        my_rect = find_image_location_in_screen(my_image)
        if my_rect:
            can_find = True
            logger.info(my_images_name_list[my_index] + ' at rect: ' + str(my_rect))
            sleep_random_time(min_time=my_delay_move_min, max_time=my_delay_move_max)
            autopy.mouse.smooth_move(my_rect[0], my_rect[1])
            logger.info('Click')
            sleep_random_time(min_time=my_delay_click_min, max_time=my_delay_click_max)
            autopy.mouse.click()
            logger.info('Move to 0,0')
            sleep_random_time(min_time=my_delay_click_min, max_time=my_delay_click_max)
            autopy.mouse.smooth_move(0, 0)
            break
    if can_find is False:
        logger.info('Not found.')


try_hide_me()
my_images_name_list = generate_image_list(my_images_directory_path)
logger.info(my_images_name_list)
my_images = []
for v in my_images_name_list:
    try:
        my_image = autopy.bitmap.Bitmap.open(os.sep.join([my_images_directory_path, v]))
        my_images.append(my_image)
    except Exception as e:
        logger.warning('Load image: ' + v + ' failed, Exception:' + str(e))
        continue
if my_images:
    try:
        while True:
            logger.info('Searching...')
            do_simulation(my_images)
            sleep_random_time(min_time=my_scan_frequency, max_time=my_scan_frequency)
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt')
else:
    logger.error('Initial failed: Can not found dir images.')
    exit()
