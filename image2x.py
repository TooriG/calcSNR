import streamlit as st
from PIL import Image, PngImagePlugin
import io
import zipfile

# 画像をリサイズする関数
def resize_image(image_file):
    with Image.open(image_file) as original_image:
        original_format = original_image.format

        # PNG metadataのコピー（PngInfoオブジェクトを使用）
        metadata = PngImagePlugin.PngInfo()
        if original_format == 'PNG':
            for k, v in original_image.info.items():
                metadata.add_text(k, v)

        size = (original_image.width * 2, original_image.height * 2)
        resized_image = original_image.resize(size, Image.Resampling.LANCZOS)

        # メモリ内のバッファに画像を保存
        img_buffer = io.BytesIO()
        if original_format == 'PNG':
            # PNG metadataを保持しながら保存
            resized_image.save(img_buffer, format='PNG', pnginfo=metadata)
        else:
            # 他のフォーマットの場合は元のフォーマットを使用して保存
            resized_image.save(img_buffer, format=original_format)
        img_buffer.seek(0)

    return img_buffer

# Streamlit UI
st.title('画像リサイズアプリ')

uploaded_files = st.file_uploader("画像をアップロードしてください", type=['jpg', 'png'], accept_multiple_files=True)

if uploaded_files:
    # Zipファイルの作成
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            img_buffer = resize_image(uploaded_file)
            # Zipファイルに追加
            zip_file.writestr(uploaded_file.name, img_buffer.read())

    # ユーザーにダウンロード用のリンクを提供
    zip_buffer.seek(0)
    st.download_button(
        label="画像をダウンロード",
        data=zip_buffer,
        file_name="resized_images.zip",
        mime="application/zip"
    )
