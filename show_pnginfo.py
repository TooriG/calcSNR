import streamlit as st
from PIL import Image
import io
import zipfile

def extract_png_info(image_path):
    """PNG画像からメタデータを抽出する関数"""
    with Image.open(image_path) as img:
        info = img.info
    return info

def remove_metadata_and_get_bytes(image_path):
    """画像からメタデータを削除して、バイトデータを返す関数"""
    with Image.open(image_path) as img:
        data = list(img.getdata())
        img_without_metadata = Image.new(img.mode, img.size)
        img_without_metadata.putdata(data)
        byte_io = io.BytesIO()
        img_without_metadata.save(byte_io, format="PNG")
    return byte_io.getvalue()

st.set_page_config(layout="wide")

st.title("PNG Metadata Extractor for Multiple Images")

uploaded_files = st.file_uploader("複数のPNG画像をアップロードしてください", type=["png"], accept_multiple_files=True)

if uploaded_files:
    all_missing_metadata = True  # デフォルトでメタデータがないとする
    for uploaded_file in uploaded_files:
        metadata = extract_png_info(uploaded_file)
        if 'parameters' in metadata:
            all_missing_metadata = False  # メタデータが存在する画像が見つかった場合

    if all_missing_metadata:
        st.warning("すべての画像にメタデータが存在しません。")

    cols = st.columns(4)  # 4列を作成

    for i, uploaded_file in enumerate(uploaded_files):
        metadata = extract_png_info(uploaded_file)
        with cols[i % 4]:
            if 'parameters' in metadata:
                st.subheader("Parameters for " + uploaded_file.name)
                parameters = metadata['parameters']
                st.text_area("", value=parameters, height=200, max_chars=None)
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
