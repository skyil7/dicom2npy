from collections import defaultdict
from typing import Union, List

import cv2
import numpy as np
import pydicom
from pydicom.dataset import FileDataset

def apply_window(image: np.array, window_level: int=-600, window_width: int =1600, dtype=np.uint8):
    img_min = window_level - window_width // 2
    img_max = window_level + window_width // 2

    windowed_image = np.clip(image, img_min, img_max)
    windowed_image = (windowed_image - img_min) / (img_max - img_min) * 255.0
    return windowed_image.astype(dtype)