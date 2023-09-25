import streamlit as st
import png
import io
import zipfile

def remove_png_metadata(png_bytes):
    reader = png.Reader(bytes=png_bytes)
    chunks = reader.chunks()
    new_chunks = [(chunk_type, data) for chunk_type, data in chunks if chunk_type not in ('tEXt', 'zTXt', 'iTXt')]
    f = io.BytesIO()
    png.write_chunks(f, new_chunks)
    return f.getvalue()

def get_png_metadata(png_bytes):
    reader = png.Reader(bytes=png_bytes)
    chunks = reader.chunks()
    metadata_chunks = [(chunk_type, data) for chunk_type, data in chunks if chunk_type in ('tEXt', 'zTXt', 'iTXt')]
    return metadata_chunks

st.title('PNGメタデータツール')

uploaded_files = st.file_uploader('PNG画像をアップロードしてください', type=['png'], accept_multiple_files=True)

if uploaded_files:
    all_files_without_metadata = []
    metadata_found = False
    for uploaded_file in uploaded_files:
        content = uploaded_file.getvalue()
        metadata = get_png_metadata(content)
        if metadata:
            metadata_found = True
            for chunk_type, data in metadata:
                st.write(f"File: {uploaded_file.name}, Chunk: {chunk_type}, Data: {data.decode('utf-8')}")
        all_files_without_metadata.append((uploaded_file.name, remove_png_metadata(content)))

    if not metadata_found:
        st.warning('すべての画像にPngメタデータがありません')

    # Create zip file with images without metadata
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in all_files_without_metadata:
            zip_file.writestr(file_name, data)

    zip_buffer.seek(0)
    st.download_button('メタデータを削除した画像をダウンロード', zip_buffer, 'without_metadata.zip')
