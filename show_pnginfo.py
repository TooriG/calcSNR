import streamlit as st
from PIL import Image
import io

def extract_png_info(image_path):
    """PNG画像からメタデータを抽出する関数"""
    with Image.open(image_path) as img:
        info = img.info
    return info

def remove_metadata_and_get_bytes(image_path):
    """画像からメタデータを削除して、バイトデータを返す関数"""
    with Image.open(image_path) as img:
        # メタデータを削除
        data = list(img.getdata())
        img_without_metadata = Image.new(img.mode, img.size)
        img_without_metadata.putdata(data)
        
        # 画像をバイトデータとして保存
        byte_io = io.BytesIO()
        img_without_metadata.save(byte_io, format="PNG")
    return byte_io.getvalue()

st.title("PNG Metadata Extractor")

uploaded_file = st.file_uploader("PNG画像をアップロードしてください", type=["png"])

if uploaded_file:
    with st.spinner("メタデータを抽出中..."):
        metadata = extract_png_info(uploaded_file)

        if 'parameters' in metadata:
            parameters = metadata['parameters']
            st.text_area("Parameters:", value=parameters, height=600)
            st.write("上のテキストをコピーしてください")
            
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

# メタデータを削除した画像をダウンロードボタンとして提供
image_bytes = remove_metadata_and_get_bytes(uploaded_file)
st.download_button("メタデータを削除した画像をダウンロード", image_bytes, file_name="image_without_metadata.png", mime="image/png")

st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

st.subheader("All Metadata")
st.write(metadata)
