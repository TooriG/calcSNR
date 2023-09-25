import streamlit as st
import os
from PIL import Image, PngImagePlugin

# メタデータの取得
def get_png_info(image):
    if "png" in image.format.lower():
        return {k: v for k, v in image.info.items() if isinstance(v, (bytes, str))}
    return {}

# メタデータを削除して画像を保存
def save_without_metadata(image, save_path):
    image = image.convert("RGBA")
    clean_image = Image.new("RGBA", image.size)
    clean_image.paste(image)
    clean_image.save(save_path, "PNG")

st.title("PNGメタデータ表示・削除ツール")

uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type="png", accept_multiple_files=True)

if uploaded_files:
    has_metadata = False
    for uploaded_file in uploaded_files:
        st.write(f"ファイル名: {uploaded_file.name}")
        with Image.open(uploaded_file) as img:
            info = get_png_info(img)
            if info:
                has_metadata = True
                st.write(info)
            else:
                st.write("この画像にはPNGメタデータがありません")

    if not has_metadata:
        st.warning("すべての画像にPNGメタデータがありません")
    else:
        save_dir = "/tmp/cleaned_images"
        os.makedirs(save_dir, exist_ok=True)
        paths = []
        for uploaded_file in uploaded_files:
            with Image.open(uploaded_file) as img:
                save_path = os.path.join(save_dir, uploaded_file.name)
                save_without_metadata(img, save_path)
                paths.append(save_path)

        st.write("メタデータを削除した画像をダウンロード:")
        for p in paths:
            st.download_button(f"{os.path.basename(p)}をダウンロード", p, "application/png")
