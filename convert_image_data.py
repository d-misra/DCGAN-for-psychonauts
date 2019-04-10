import os
import os.path

import cv2
import numpy as np

from images_utils import get_images_recursively
from utils import convert_to_hsl


def imread(path):
  img_bgr = cv2.imread(path)
  img_rgb = img_bgr[..., ::-1]
  # img_hsl = convert_to_hsl(img_rgb)
  return img_rgb.astype(np.float)


def normalize_rgb(image):
  return np.array(image) / 127.5 - 1.


def is_normalized(image):
  for x, row in enumerate(image):
    for y, p in enumerate(row):
      if p[0] < -1 or p[0] > 1:
        return False

  return True


def create_folder_is_not_exists(folder):
  if not os.path.exists(folder):
    os.mkdir(folder)


def convert_to_files(data_set):
  images_paths = get_images_recursively('data/' + data_set)

  data_set_rgb = data_set + '-rgb'
  data_set_hsl = data_set + '-hsl'

  create_folder_is_not_exists('data/' + data_set_hsl)
  create_folder_is_not_exists('data/' + data_set_rgb)

  count = 0
  for image_path in images_paths:
    rgb = imread(image_path)
    rgb_normalized = normalize_rgb(rgb)
    hsl = convert_to_hsl(rgb)
    rgb_normalized.tofile('data/' + data_set_rgb + '/' + str(count))
    hsl.tofile('data/' + data_set_hsl + '/' + str(count))
    count += 1


#convert_to_files('4-People-100x150_small')
