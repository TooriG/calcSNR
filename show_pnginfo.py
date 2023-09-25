import streamlit as st
from PIL import Image, PngImagePlugin
import io
import base64

def get_image_data(image):
    pnginfo_dict = {}
    for k, v in image.info.items():
        if isinstance(v, PngImagePlugin.PngInfo):
            for key in v:
                pnginfo_dict[key] = v[key].decode()
    return pnginfo_dict

def remove_png_info(image):
    return Image.open(io.BytesIO(image.tobytes()))

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href

st.title("PNG画像のメタデータ情報")

uploaded_files = st.file_uploader("PNG画像を選択してください", type="png", accept_multiple_files=True)

if uploaded_files:
    clean_images = []
    has_metadata = False

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        metadata = get_image_data(image)

        if metadata:
            has_metadata = True
            st.write(f"{uploaded_file.name} のメタデータ:")
            st.write(metadata)
        else:
            st.write(f"{uploaded_file.name} にはメタデータがありません。")

        clean_image = remove_png_info(image)
        byte_io = io.BytesIO()
        clean_image.save(byte_io, format="PNG")
        clean_images.append(byte_io.getvalue())

    if has_metadata:
        st.markdown(get_binary_file_downloader_html("clean_images.zip", "メタデータを削除した画像をダウンロード"), unsafe_allow_html=True)
    else:
        st.warning("すべての画像にPngメタデータがありません")
