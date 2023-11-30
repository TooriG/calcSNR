import streamlit as st
from PIL import Image
import zipfile
import io
import os

# Function to resize image
def resize_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

st.title('Folder Image Resizer')

# File uploader for ZIP files
uploaded_files = st.file_uploader("Upload ZIP files containing image folders", accept_multiple_files=True, type=['zip'])

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for uploaded_file in uploaded_files:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_in:
                for file in zip_in.namelist():
                    # Check if the file is an image
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        with zip_in.open(file) as img_file:
                            # Resize image and get byte data
                            img_data = resize_image(img_file)
                            # Write the resized image to the output ZIP
                            zip_out.writestr(file, img_data)

    # Reset buffer position and create download button
    zip_buffer.seek(0)
    st.download_button(
        label="Download Resized Images",
        data=zip_buffer,
        file_name="resized_images.zip",
        mime="application/zip"
    )
