import streamlit as st
from PIL import Image
import io
import zipfile

def extract_png_info(image_path):
    """PNG画像からメタデータを抽出する関数"""
    with Image.open(image_path) as img:
        info = img.info
    return info

def remove_metadata_and_get_bytes(image):
    """画像からメタデータを削除して、バイトデータを返す関数"""
    data = list(image.getdata())
    img_without_metadata = Image.new(image.mode, image.size)
    img_without_metadata.putdata(data)
        
    # 画像をバイトデータとして保存
    byte_io = io.BytesIO()
    img_without_metadata.save(byte_io, format="PNG")
    return byte_io.getvalue()

st.set_page_config(layout="wide")  # UIの横幅を広く取る

st.title("PNG Metadata Extractor")

uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type=["png"], accept_multiple_files=True)

if uploaded_files:
    zipped_file = io.BytesIO()
    with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zf:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            img_data = remove_metadata_and_get_bytes(Image.open(uploaded_file))
            zf.writestr(file_name, img_data)
    zipped_file.seek(0)
    
    st.download_button(
        "メタデータを削除した画像を一括ダウンロード",
        zipped_file,
        file_name="images_without_metadata.zip",
        mime="application/zip"
    )

    for uploaded_file in uploaded_files:
        with st.spinner(f"{uploaded_file.name}のメタデータを抽出中..."):
            metadata = extract_png_info(uploaded_file)

        col1, col2 = st.columns([1, 2])  # 画像とメタデータのカラム

        with col1:
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

        with col2:
            if 'parameters' in metadata:
                st.subheader(f"{uploaded_file.name} - Parameters")
                parameters = metadata['parameters']
                st.text_area("", value=parameters, height=300)
