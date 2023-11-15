import streamlit as st
from PIL import Image

st.title('PNG Parameters Metadata Viewer')

# ファイルアップローダーを作成
uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type=['png'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with Image.open(uploaded_file) as img:
            # 'parameters' メタデータの有無を確認
            if "parameters" in img.info:
                st.subheader(f"{uploaded_file.name}の 'parameters' メタデータ")
                # テキストボックスにメタデータを表示
                st.text_area("メタデータ内容", img.info["parameters"], height=150)
            else:
                # 'parameters' メタデータがない場合
                st.text(f"{uploaded_file.name}に 'parameters' メタデータはありません。")
