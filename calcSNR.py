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
    st.title('画像分析アプリ')

    # 画像のアップロード
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png"])
    
    if uploaded_file is not None:
        # 画像を読み込む
        image = Image.open(uploaded_file)
        # 画像を表示
        st.image(image, caption='アップロードされた画像', use_column_width=True)
        
        # 画像分析
        mean, std, histogram = analyze_image(image)
        
        # 分析結果を表示
        st.write(f"平均（Mean）: {mean:.2f}")
        st.write(f"標準偏差（Standard Deviation）: {std:.2f}")

        # ヒストグラムを表示
        fig, ax = plt.subplots()
        ax.bar(range(256), histogram, color='gray')
        ax.set_title('Image Histogram')
        ax.set_xlabel('Pixel Value')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

if __name__ == "__main__":
    main()
