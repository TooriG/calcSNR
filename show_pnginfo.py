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

st.set_page_config(layout="wide")  # UIの横幅を広く取る

st.title("PNG Metadata Extractor for Multiple Images")

uploaded_files = st.file_uploader("複数のPNG画像をアップロードしてください", type=["png"], accept_multiple_files=True)

if uploaded_files:
    # 一括ダウンロード用のZIPファイルを作成
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as z:
        for uploaded_file in uploaded_files:
            image_bytes = remove_metadata_and_get_bytes(uploaded_file)
            z.writestr(uploaded_file.name, image_bytes)
    zip_buffer.seek(0)
    st.download_button("メタデータを削除した画像を一括ダウンロード", zip_buffer, file_name="images_without_metadata.zip", mime="application/zip")
    
    for uploaded_file in uploaded_files:
        metadata = extract_png_info(uploaded_file)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        
        with col2:
            if 'parameters' in metadata:
                st.subheader("Parameters for " + uploaded_file.name)
                parameters = metadata['parameters']
                st.text_area("", value=parameters, height=200, max_chars=None)
