import glob
import os
import random

import cv2
import numpy as np


def get_boxes(sample_res, render_res):
  if sample_res[0] % render_res[0] != 0 or sample_res[1] % render_res[1] != 0:
    print('Error: Resolution not divisible: {}, {}'.format(sample_res, render_res))
    exit(1)

  boxes = []
  x_cuts = int(sample_res[0] / render_res[0])
  y_cuts = int(sample_res[1] / render_res[1])
  for x in range(0, x_cuts):
    for y in range(0, y_cuts):
      x1 = x * render_res[0]
      y1 = y * render_res[1]
      x2 = (x + 1) * render_res[0]
      y2 = (y + 1) * render_res[1]
      boxes.append([x1, y1, x2, y2])

  return boxes


def get_images_recursively(image_folder):
  images = []
  images.extend(glob.iglob(image_folder + '/**/*.jpg', recursive=True))
  images.extend(glob.iglob(image_folder + '/**/*.jpeg', recursive=True))
  images.extend(glob.iglob(image_folder + '/**/*.png', recursive=True))
  return images


def imread(path):
  img_bgr = cv2.imread(path)
  img_rgb = img_bgr[..., ::-1]
  # img_hsl = convert_to_hsl(img_rgb)
  return img_rgb.astype(np.float)


def normalize_rgb(image):
  return np.array(image) / 127.5 - 1.


class DataSetManager:
  def __init__(self, base_folder, enable_cache, color_model):
    self.base_folder = base_folder
    self.enable_cache = enable_cache
    self.color_model = color_model
    self.rgb_np_file_folder = 'data/' + base_folder + '-rgb'
    self.hsl_np_file_folder = 'data/' + base_folder + '-hsl'
    self.has_rgb_np_file_cache = os.path.exists(self.rgb_np_file_folder)
    self.has_hsl_np_file_cache = os.path.exists(self.hsl_np_file_folder)
    self.images_paths = get_images_recursively('data/' + base_folder)
    self.image_cache = []
    if self.enable_cache:
      self.cache()

  def cache(self):
    if self.color_model == 'rgb':
      for image_path in self.images_paths:
        self.image_cache.append(normalize_rgb(imread(image_path)))

  def get_random_image(self):
    if self.enable_cache:
      idx = random.randint(0, len(self.image_cache) - 1)
      print('image {} loaded from cache'.format(idx))
      return self.image_cache[idx]
    elif self.color_model == 'rgb':
      if self.has_rgb_np_file_cache:
        nbr_of_elements = len([name for name in os.listdir(self.rgb_np_file_folder) if os.path.isfile(name)])
        idx = random.randint(0, nbr_of_elements - 1)
        np_file_path = self.rgb_np_file_folder + '/' + idx
        print('image loaded from ' + np_file_path)
        return np.load(np_file_path)
      elif not self.has_rgb_np_file_cache:
        idx = random.randint(0, len(self.images_paths) - 1)
        image_path = self.images_paths[idx]
        print('image loaded from ' + image_path)
        return normalize_rgb(imread(image_path))

  def get_random_images(self, nbr):
    result = []
    for _ in range(0, nbr):
      result.append(self.get_random_image())

    return result
