import glob
import os
from collections import defaultdict
from typing import Union, List

import numpy as np
import pydicom
from pydicom.dataset import FileDataset

def load_dicom_files(folder_path: str) -> dict:
    """
    경로 안의 dicom 파일들을 읽어, 같은 촬영본끼리 그룹화하여 return합니다.
    """
    dicom_groups = defaultdict(list)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.dcm'):
            file_path = os.path.join(folder_path, filename)
            dicom_file = pydicom.dcmread(file_path)
            
            # 시리즈 인스턴스 UID를 기준으로 그룹화
            series_uid = dicom_file.SeriesInstanceUID
            dicom_groups[series_uid].append(dicom_file)
    
    # dicom 이미지를 순서대로 정렬
    dicom_groups = {uid:sorted(group, key=lambda x: x.InstanceNumber, reverse=True) for uid, group in dicom_groups.items()}

    print(f"Found {len(dicom_groups)} series of images: total {len(os.listdir(folder_path))} slides")
    return dicom_groups

def dicom2npy(dicom_images: Union[FileDataset, List[FileDataset]]) -> np.array:
    """
    하나의 슬라이드, 혹은 여러 개의 dicom 파일을 읽어 numpy array로 변환합니다.
    """
    if isinstance(dicom_images, list):
        images = []
        for dcm in dicom_images:
            images.append(dcm.pixel_array)
        return np.stack(images)  # 3D
    return dcm.pixel_array  # 2D slide
    