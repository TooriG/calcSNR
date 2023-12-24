import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 画像のノイズ特性を計算する関数
def analyze_image(image):
    # 画像をグレースケールに変換し、NumPy配列にする
    gray_image = np.array(image.convert('L'))

    # 平均と標準偏差を計算
    mean = np.mean(gray_image)
    std = np.std(gray_image)

    # ヒストグラムを計算（256階調）
    histogram, _ = np.histogram(gray_image, bins=256)

    return mean, std, histogram

# Streamlitアプリケーションのメイン関数
def main():
    st.title('Image Analysis App')

    # 複数の画像のアップロード
    uploaded_files = st.file_uploader("Please upload images", type=["jpg", "png"], accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:
        # カラムを作成して、画像と分析結果を横に表示
        col1, col2 = st.columns(2)
        
        with col1:  # 画像の表示
            image = Image.open(uploaded_file)
            st.image(image, caption=f'Uploaded Image: {uploaded_file.name}', use_column_width=True)
        
        with col2:  # 画像分析と結果の表示
            mean, std, histogram = analyze_image(image)
            st.write(f"Mean: {mean:.2f}")
            st.write(f"Standard Deviation: {std:.2f}")
            
            # ヒストグラムを表示
            fig, ax = plt.subplots()
            ax.bar(range(256), histogram, color='gray')
            ax.set_title('Image Histogram')
            ax.set_xlabel('Pixel Value')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)

if __name__ == "__main__":
    main()
