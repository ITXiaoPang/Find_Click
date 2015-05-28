# -*- coding: utf-8 -*-
__author__ = 'ITXiaoPang'

from autopy import bitmap
from autopy import mouse
from time import sleep
from random import uniform
from os import getcwd,sep,listdir
from os.path import exists

# Config
my_images_directory_name = r'images'
my_tolerance = 0.0
my_scan_frequency = 5
my_delay_move_min = 2
my_delay_move_max = 5
my_delay_click_min = 0
my_delay_click_max = 1

def sleep_random_time(min_time=1,max_time=10):
    my_random_time = uniform(min_time,max_time)
    print('Sleep:' + str(my_random_time))
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
    return my_rect


def do_simulation(my_images):
    for my_image in my_images:
        my_rect = find_image_location_in_screen(my_image)
        if my_rect:
            sleep_random_time(min_time=my_delay_move_min,max_time=my_delay_move_max)
            print('Rect: ' + str(my_rect))
            mouse.smooth_move(my_rect[0],my_rect[1])
            sleep_random_time(min_time=my_delay_click_min,max_time=my_delay_click_max)
            mouse.click()
            break


if __name__ == '__main__':
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
            do_simulation(my_images)
            sleep(my_scan_frequency)
    else:
        print('Initial failed: Can not found dir images.')
        exit()
