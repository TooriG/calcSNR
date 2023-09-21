import streamlit as st
from PIL import Image

def extract_png_info(image_path):
    """PNG画像からメタデータを抽出する関数"""
    with Image.open(image_path) as img:
        info = img.info
    return info

st.title("PNG Metadata Extractor")

uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])

if uploaded_file:
    with st.spinner("メタデータを抽出中..."):
        metadata = extract_png_info(uploaded_file)
        
        if "comment" in metadata:
            st.subheader("Comment")
            st.write(metadata["comment"])
        
        if "title" in metadata:
            st.subheader("Title")
            st.write(metadata["title"])
        
        if "author" in metadata:
            st.subheader("Author")
            st.write(metadata["author"])
        
        if "description" in metadata:
            st.subheader("Description")
            st.write(metadata["description"])
        
        if "software" in metadata:
            st.subheader("Software")
            st.write(metadata["software"])
        
        st.subheader("All Metadata")
        st.write(metadata)

