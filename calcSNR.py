import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# RGBチャネルのヒストグラムと統計情報を計算する関数
def analyze_color_image(image):
    # NumPy配列にする
    image_array = np.array(image)

    # RGBチャネルを分割
    red_channel = image_array[:, :, 0]
    green_channel = image_array[:, :, 1]
    blue_channel = image_array[:, :, 2]

    # RGBチャネルの平均と標準偏差を計算
    mean_red, std_red = np.mean(red_channel), np.std(red_channel)
    mean_green, std_green = np.mean(green_channel), np.std(green_channel)
    mean_blue, std_blue = np.mean(blue_channel), np.std(blue_channel)

    # RGBチャネルのヒストグラムを計算（256階調）
    histogram_red, _ = np.histogram(red_channel, bins=256, range=(0, 256))
    histogram_green, _ = np.histogram(green_channel, bins=256, range=(0, 256))
    histogram_blue, _ = np.histogram(blue_channel, bins=256, range=(0, 256))

    return (mean_red, std_red, histogram_red), (mean_green, std_green, histogram_green), (mean_blue, std_blue, histogram_blue)

# Streamlitアプリケーションのメイン関数
def main():
    st.title('Color Image Analysis App')

    # 複数の画像のアップロード
    uploaded_files = st.file_uploader("Please upload images", type=["jpg", "png"], accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:
        # カラムを作成して、画像と分析結果を横に表示
        col1, col2 = st.columns(2)
        
        with col1:  # 画像の表示
            image = Image.open(uploaded_file)
            st.image(image, caption=f'Uploaded Image: {uploaded_file.name}', use_column_width=True)
        
        with col2:  # 画像分析と結果の表示
            # RGBチャネルの分析
            (mean_red, std_red, histogram_red), \
            (mean_green, std_green, histogram_green), \
            (mean_blue, std_blue, histogram_blue) = analyze_color_image(image)

            # 平均と標準偏差の表示
            st.write(f"Mean Red: {mean_red:.2f}, Std Red: {std_red:.2f}")
            st.write(f"Mean Green: {mean_green:.2f}, Std Green: {std_green:.2f}")
            st.write(f"Mean Blue: {mean_blue:.2f}, Std Blue: {std_blue:.2f}")

            # ヒストグラムを表示
            fig, ax = plt.subplots()
            ax.plot(histogram_red, color='red', label='Red Channel')
            ax.plot(histogram_green, color='green', label='Green Channel')
            ax.plot(histogram_blue, color='blue', label='Blue Channel')
            ax.set_title('Color Histogram')
            ax.set_xlabel('Pixel Intensity')
            ax.set_ylabel('Frequency')
            ax.legend()
            st.pyplot(fig)

if __name__ == "__main__":
    main()
