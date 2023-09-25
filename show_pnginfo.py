import streamlit as st
from PIL import Image
import io
import zipfile

st.title('PNG Metadata Remover')

uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type=['png'], accept_multiple_files=True)

if uploaded_files:
    images_without_metadata = []
    metadata_detected = False
    
    for uploaded_file in uploaded_files:
        with Image.open(uploaded_file) as img:
            # メタデータを削除
            if img.info:
                metadata_detected = True
            data = io.BytesIO()
            img.save(data, format="PNG")
            images_without_metadata.append((uploaded_file.name, data.getvalue()))

    if metadata_detected:
        st.write('メタデータを検出しました。ダウンロード準備中...')
        
        # すべての画像をZIPファイルにまとめる
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as z:
            for name, data in images_without_metadata:
                z.writestr(name, data)
        
        st.download_button('ダウンロード', zip_buffer.getvalue(), 'images_without_metadata.zip')
    else:
        st.warning('すべての画像にPNGメタデータがありません')
