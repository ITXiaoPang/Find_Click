# -*- coding: utf-8 -*-
__author__ = 'ITXiaoPang'

from autopy import bitmap
from autopy import mouse
from time import sleep
from random import uniform
from os import getcwd,sep,listdir
from os.path import exists
import ctypes


# Config
my_hide = False
my_images_directory_name = r'images'
my_tolerance = 0.0
my_scan_frequency = 5
my_delay_move_min = 2
my_delay_move_max = 10
my_delay_click_min = 0
my_delay_click_max = 1

if my_hide:
    whnd = ctypes.windll.kernel32.GetConsoleWindow()   
    if whnd != 0:
        pass
        ctypes.windll.user32.ShowWindow(whnd, 0)   
        ctypes.windll.kernel32.CloseHandle(whnd) 


def sleep_random_time(min_time=1,max_time=10):
    my_random_time = uniform(min_time,max_time)
    print(str(my_random_time).join(['Sleep: ',' seconds']))
    sleep(my_random_time)


def generate_image_list(my_images_directory_path):
    if exists(my_images_directory_path):
        my_image_files_name_list = listdir(my_images_directory_path)
    else:
        my_image_files_name_list = None
    return my_image_files_name_list


def find_image_location_in_screen(my_image):
    my_screen = bitmap.capture_screen()
    my_rect = my_screen.find_bitmap(my_image, my_tolerance)
    if my_rect:
        my_rect = list(my_rect)
        my_rect[0]+=my_image.width / 2
        my_rect[1]+=my_image.height / 2
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
            print(my_images_name_list[my_index] + ' at rect: ' + str(my_rect))
            sleep_random_time(min_time=my_delay_move_min,max_time=my_delay_move_max)
            mouse.smooth_move(my_rect[0],my_rect[1])
            print('Click')
            sleep_random_time(min_time=my_delay_click_min,max_time=my_delay_click_max)
            mouse.click()
            print('Move to 0,0')
            sleep_random_time(min_time=my_delay_click_min,max_time=my_delay_click_max)
            mouse.smooth_move(0,0)
            break
    if can_find is False:
        print('Not found.')


my_images_directory_path = sep.join([getcwd(),my_images_directory_name])
my_images_name_list = generate_image_list(my_images_directory_path)
print(my_images_name_list)
my_images = []
for v in my_images_name_list:
    try:
        my_image = bitmap.Bitmap.open(sep.join([my_images_directory_path, v]))
        my_images.append(my_image)
    except Exception,e:
        print('Load image: ' + v + ' failed, Exception:' + str(e))
        continue
if my_images:
    while True:
        print('Searching...')
        do_simulation(my_images)
        sleep_random_time(min_time=my_scan_frequency,max_time=my_scan_frequency)
else:
    print('Initial failed: Can not found dir images.')
    exit()
