import streamlit as st
from dicom2npy.utils import *
import plotly.graph_objects as go

def render_image(dcm_img):
    left, right = st.columns([1, 1])
    with right:
        axis = st.slider("axis", min_value=0, max_value=2)
        n = st.slider("n_slide", min_value=0, max_value=dcm_img.shape[axis])

        ww = st.slider("window width (ww)", min_value=0, max_value=4095, value=2800)
        wl = st.slider("window level (wl)", min_value=-1024, max_value=3071, value=600)
    dcm_img_slide = get_slide(dcm_img, n, axis)
    dcm_img_slide_ = apply_window(dcm_img_slide, window_width=ww, window_level=wl)

    with left:
        fig = go.Figure(data=go.Heatmap(
            z=dcm_img_slide_,
            colorscale='Gray',
            showscale=False,
            hoverinfo='z',
            customdata=dcm_img_slide,
            hovertemplate='pixel value: %{customdata}'
        ))

        fig.update_layout(
            title='CT Image',
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            width=1000,height=1000
        )
        fig.update_layout(yaxis_scaleanchor="x")

        # Streamlit에 Plotly 그래프 표시
        st.plotly_chart(fig, use_container_width=True, height=1500)
