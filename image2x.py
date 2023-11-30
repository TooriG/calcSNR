import streamlit as st
from PIL import Image
import io
import zipfile

def resize_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

st.title('Folder Image Resizer')

uploaded_file = st.file_uploader("Upload a ZIP file containing images", type=['zip'])

if uploaded_file:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_in:
            for file in zip_in.namelist():
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    with zip_in.open(file) as img_file:
                        img_data = resize_image(img_file)
                        zip_out.writestr(file, img_data)

    zip_buffer.seek(0)
    st.download_button(
        label="Download Resized Images",
        data=zip_buffer,
        file_name="resized_folder_images.zip",
        mime="application/zip"
    )
