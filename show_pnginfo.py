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
    all_images_lack_metadata = True
    for uploaded_file in uploaded_files:
        metadata = extract_png_info(uploaded_file)
        if 'parameters' in metadata:
            all_images_lack_metadata = False
            break

    if all_images_lack_metadata:
        st.error("すべての画像にメタデータが存在しません。")

    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as z:
            for uploaded_file in uploaded_files:
                image_bytes = remove_metadata_and_get_bytes(uploaded_file)
                z.writestr(uploaded_file.name, image_bytes)
        zip_buffer.seek(0)
        st.download_button("メタデータを削除した画像を一括ダウンロード", zip_buffer, file_name="images_without_metadata.zip", mime="application/zip")
    
    for i in range(0, len(uploaded_files), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            metadata1 = extract_png_info(uploaded_files[i])
            st.image(uploaded_files[i], caption="Uploaded Image.", use_column_width=True)
            if 'parameters' in metadata1:
                st.text_area("", value=metadata1['parameters'], height=200, max_chars=None)

        if i + 1 < len(uploaded_files):  # 画像が奇数の場合、最後の列を確認
            with col2:
                metadata2 = extract_png_info(uploaded_files[i + 1])
                st.image(uploaded_files[i + 1], caption="Uploaded Image.", use_column_width=True)
                if 'parameters' in metadata2:
                    st.text_area("", value=metadata2['parameters'], height=200, max_chars=None)
