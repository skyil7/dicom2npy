from collections import defaultdict
from typing import Union, List

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

def thresholding_otsu(img: np.array, min_val=-1024., max_val=2048.):
    """
    Otsu의 이진화를 사용한 노이즈 제거
    """
    row_size = img.shape[0]
    col_size = img.shape[1]

    img_ = np.clip(img, min_val, max_val)
    img_ = ((img_ - min_val) / (max_val - min_val))  # 0~1로 이동

    # 마스킹을 위한 이미지 생성
    int_img = img_ * 255
    int_img = int_img.astype(np.uint8)

    # Otsu의 이진화 (Thresholding)
    _, thresholded_cbct = cv2.threshold(int_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 형태학적 연산 (Morphological Operations)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 타원형 커널 사용
    closed_cbct = cv2.morphologyEx(thresholded_cbct, cv2.MORPH_CLOSE, kernel)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed_cbct)

    # 가장 큰 구성 요소 선택 (Largest Component Selection)
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    mask_cbct = np.zeros_like(int_img, dtype=np.uint8)
    mask_cbct[labels == largest_label] = 255

    # 원본 이미지 마스킹 (Masking Original Image)
    img[mask_cbct == 0] = 0

    return img