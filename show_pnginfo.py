import streamlit as st
import os
import io
from purepng import png

def remove_metadata_from_png(png_data):
    reader = png.Reader(bytes=png_data)
    d = reader.asDirect()
    out = io.BytesIO()
    w = png.Writer(d[0], d[1], greyscale=d[3]['greyscale'], alpha=d[3]['alpha'], bitdepth=d[3]['bitdepth'])
    w.write(out, d[2])
    return out.getvalue()

def extract_png_info(png_data):
    info = []
    for chunk in png.Reader(bytes=png_data).chunks():
        if chunk[0] == b'tEXt':
            info.append(chunk[1].decode('latin1'))
    return info

st.title("PNG Metadata Extractor & Remover")

uploaded_files = st.file_uploader("Upload PNG files", type=["png"], accept_multiple_files=True)

if uploaded_files:
    meta_info_found = False
    cleaned_files = {}
    
    for f in uploaded_files:
        file_bytes = f.read()
        info = extract_png_info(file_bytes)
        if info:
            meta_info_found = True
            st.write(f"**{f.name}**")
            for i in info:
                st.text(i)
        cleaned_files[f.name] = remove_metadata_from_png(file_bytes)
    
    if not meta_info_found:
        st.header("すべての画像にPngメタデータがありません")
    
    def get_all_files():
        with io.BytesIO() as buffer:
            with zipfile.ZipFile(buffer, 'a', zipfile.ZIP_DEFLATED) as z:
                for name, data in cleaned_files.items():
                    z.writestr(name, data)
            return buffer.getvalue()

    if st.button('Cleaned PNGs Download'):
        files = get_all_files()
        st.download_button("Download cleaned PNGs", files, "cleaned_pngs.zip")
