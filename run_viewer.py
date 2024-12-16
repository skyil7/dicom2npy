import os
import glob

import streamlit as st

from dicom2npy.utils import *
from dicom2npy.viewer import *

directories = []
for root, dirs, files in  os.walk("dataset"):
    if len(dirs) == 0:
        directories.append(root)

st.set_page_config(layout="wide")
st.write("# CT Image Viewer")

target_dir = st.selectbox("탐색할 경로", options=directories)
dicoms = load_dicom_files(target_dir)

target_img = st.selectbox("이미지", options=dicoms.keys())
dcm_img = dicom2npy(dicoms[target_img])

if dcm_img is not None:
    render_image(dcm_img)