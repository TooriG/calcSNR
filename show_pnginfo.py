import streamlit as st
from PIL import Image
import io
import zipfile

def strip_png_metadata(img):
    data = io.BytesIO()
    img.save(data, "PNG", compress_level=9)
    return data

st.title('PNGメタデータ削除ツール')

uploaded_files = st.file_uploader("PNG画像をアップロードしてください", type=['png'], accept_multiple_files=True)

if uploaded_files:
    stripped_data = []
    all_images_without_metadata = True
    
    for file in uploaded_files:
        with Image.open(file) as img:
            # Check for metadata
            if 'tEXt' in img.info:
                all_images_without_metadata = False
                st.write(f"{file.name} のメタデータ:")
                for key, value in img.info['tEXt'].items():
                    st.write(f"{key}: {value}")
            else:
                st.write(f"{file.name} にはメタデータがありません。")

            stripped_data.append((file.name, strip_png_metadata(img)))
    
    if all_images_without_metadata:
        st.warning("すべての画像にPngメタデータがありません")
    else:
        with st.spinner('画像の処理中...'):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'a', zipfile.ZIP_DEFLATED, False) as z:
                for name, data in stripped_data:
                    data.seek(0)
                    z.writestr(name, data.getvalue())
            buffer.seek(0)
            st.success('完了!')
            st.download_button('画像をダウンロード', buffer, file_name='stripped_images.zip', mime='application/zip')
