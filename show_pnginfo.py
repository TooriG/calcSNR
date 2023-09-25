import streamlit as st
import os
import shutil
import tempfile
from PIL import Image

# 画像のメタデータを削除する関数
def remove_metadata(img_path):
    with Image.open(img_path) as image:
        image_data = image.tobytes()
        image_without_metadata = Image.frombytes(image.mode, image.size, image_data)
        image_without_metadata.save(img_path)

# アプリのタイトル
st.title("PNG Metadata Remover")

# 複数の画像をアップロード
uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type="png", accept_multiple_files=True)

if uploaded_files:
    metadata_found = False

    # 一時ディレクトリを作成
    temp_dir = tempfile.mkdtemp()

    for file in uploaded_files:
        # 画像の情報を表示
        with Image.open(file) as image:
            st.write(f"File: {file.name}")
            st.write("Size:", image.size)
            st.write("Mode:", image.mode)
            if image.info:
                metadata_found = True
                st.write("Metadata:", image.info)
            else:
                st.write("This image has no metadata.")
            st.image(image, caption=file.name, use_column_width=True)
        
        # メタデータを削除して一時ディレクトリに保存
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        remove_metadata(file_path)

    # メタデータが見つかった場合、ダウンロードボタンを表示
    if metadata_found:
        with st.spinner("Creating a downloadable zip..."):
            # 画像をzipファイルにパッケージング
            shutil.make_archive("/tmp/images_without_metadata", 'zip', temp_dir)
        st.download_button(label="PNGメタデータを削除した画像をダウンロード", data="/tmp/images_without_metadata.zip", file_name="images_without_metadata.zip")
    else:
        st.error("すべての画像にPngメタデータがありません")

    # 一時ディレクトリを削除
    shutil.rmtree(temp_dir)
