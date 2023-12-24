import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# RGBチャネルのヒストグラムを計算する関数
def calculate_histograms(image):
    # NumPy配列に変換
    image_array = np.array(image)

    # RGBチャネルごとのヒストグラムを計算
    red_hist, bins = np.histogram(image_array[:,:,0], bins=256, range=[0,256])
    green_hist, _ = np.histogram(image_array[:,:,1], bins=256, range=[0,256])
    blue_hist, _ = np.histogram(image_array[:,:,2], bins=256, range=[0,256])
    
    return red_hist, green_hist, blue_hist, bins

# ヒストグラムを表示する関数
def plot_histograms(red_hist, green_hist, blue_hist, bins):
    plt.figure(figsize=(10, 4))
    plt.title('Color Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')

    plt.bar(bins[:-1] - 0.75, red_hist, color='red', alpha=0.6, label='Red', width=0.5)
    plt.bar(bins[:-1] - 0.25, green_hist, color='green', alpha=0.6, label='Green', width=0.5)
    plt.bar(bins[:-1] + 0.25, blue_hist, color='blue', alpha=0.6, label='Blue', width=0.5)
    
    plt.legend()
    return plt

# Streamlitアプリケーションのメイン関数
def main():
    st.title('Color Image Histogram Analysis')

    # 複数の画像のアップロード
    uploaded_files = st.file_uploader("Please upload color images", type=["jpg", "png"], accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:
        # カラムを作成して、画像とヒストグラムを横に表示
        col1, col2 = st.columns(2)
        
        with col1:  # 画像の表示
            image = Image.open(uploaded_file)
            st.image(image, caption=f'Uploaded Image: {uploaded_file.name}', use_column_width=True)
        
        with col2:  # ヒストグラムの表示
            red_hist, green_hist, blue_hist, bins = calculate_histograms(image)
            plt = plot_histograms(red_hist, green_hist, blue_hist, bins)
            st.pyplot(plt)

if __name__ == "__main__":
    main()
