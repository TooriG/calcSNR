import streamlit as st
from PIL import Image
import io
import zipfile

# Function to resize the image
def resize_image(image):
    original_image = Image.open(image)
    size = (original_image.width * 2, original_image.height * 2)
    resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
    return resized_image

# Streamlit application interface
st.title('Image Resizer Web App')

# Multiple file uploader
uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files:
    # In-memory buffer for the zip file
    zip_buffer = io.BytesIO()

    # Create a zip file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            # Resize the image
            image = resize_image(uploaded_file)

            # In-memory buffer for the resized image
            img_buffer = io.BytesIO()
            image.save(img_buffer, format=image.format)
            img_buffer.seek(0)

            # Add the image to the zip file
            zip_file.writestr(uploaded_file.name, img_buffer.getvalue())

    # Reset the buffer's cursor to the beginning
    zip_buffer.seek(0)

    # Download button
    st.download_button(
        label="Download Resized Images",
        data=zip_buffer,
        file_name="resized_images.zip",
        mime='application/zip'
    )
