import streamlit as st
from PIL import Image

st.title('PNG Metadata Viewer')

# ファイルアップローダーを作成
uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type=['png'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with Image.open(uploaded_file) as img:
            # メタデータの有無を確認
            if img.info:
                st.subheader(f"{uploaded_file.name}のメタデータ")
                for key, value in img.info.items():
                    st.text(f"{key}: {value}")
            else:
                # メタデータがない場合
                st.text(f"{uploaded_file.name}にメタデータはありません。")
