import streamlit as st
from PIL import Image
import numpy as np

# 画像のノイズを判断する関数
def calculate_noise(image):
    # 画像をグレースケールに変換し、NumPy配列にする
    image = np.array(image.convert('L'))
    # 画像の平均と標準偏差を計算
    mean = np.mean(image)
    std = np.std(image)
    # 信号対雑音比（SNR）を計算
    snr = mean / std if std != 0 else 0
    return snr

# Streamlitアプリケーションのメイン関数
def main():
    st.title('画像ノイズ判定アプリ')

    # 複数の画像のアップロード
    uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "png"], accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            # 画像を読み込む
            image = Image.open(uploaded_file)
            # 画像を表示
            st.image(image, caption='アップロードされた画像', use_column_width=True)
            
            # ノイズを計算
            snr = calculate_noise(image)
            # 結果を表示
            st.write(f"{uploaded_file.name} の信号対雑音比 (SNR): {snr:.2f}")

if __name__ == "__main__":
    main()
