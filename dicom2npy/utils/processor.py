from collections import defaultdict
from typing import Union, List, Iterable

import cv2
import numpy as np
import pydicom
from pydicom.dataset import FileDataset

def get_slide(numpy_volume: np.array, n=0, axis=0) -> np.array:
    """
    3d volume을 정면, 측면, 상단 등 각 각도에서 바라본 n번째 슬라이드를 추출합니다.
    """
    assert len(numpy_volume.shape) == 3
    if axis == 0:
        return numpy_volume[n, :, :]
    if axis == 1:
        return numpy_volume[:, n, :]
    return numpy_volume[:, :, n]

def shift_value(img: np.array, source=(-1024, 3071), target=(0, 255), dtype=np.int16):
    img = np.clip(img, source[0], source[1])
    img = ((img - source[0]) / (source[1] - source[0]))
    img = img * (target[1] - target[0])
    img = img + target[0]
    return img.astype(dtype)

def thresholding_otsu(img: np.array, min_val:float =-1024., max_val:float =3071.):
    """
    Otsu의 이진화를 사용한 노이즈 제거
    """
    row_size = img.shape[0]
    col_size = img.shape[1]

    int_img = shift_value(img, source=(min_val, max_val), target=(0, 255))

    # Otsu의 이진화 (Thresholding)
    _, thresholded_img = cv2.threshold(int_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 형태학적 연산 (Morphological Operations)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 타원형 커널 사용
    closed_img = cv2.morphologyEx(thresholded_img, cv2.MORPH_CLOSE, kernel)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed_img)

    # 가장 큰 구성 요소 선택 (Largest Component Selection)
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    mask_img = np.zeros_like(int_img, dtype=np.uint8)
    mask_img[labels == largest_label] = 255

    # 원본 이미지 마스킹 (Masking Original Image)
    img[mask_img == 0] = 0

    return img