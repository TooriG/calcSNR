# -*- coding: utf-8 -*-

import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# 画像を取得するためのAPIエンドポイント
API_ENDPOINT = "https://api.unsplash.com/photos/random?client_id=AbkbZ5qQ-hd5bzJ1nZ4NB7Ko8F6D8__ALTS0F8jXOko"

# ランダムな画像を取得するための関数
def get_random_image():
    response = requests.get(API_ENDPOINT)
    response.raise_for_status()
    image_url = response.json()["urls"]["regular"]
    return image_url

# アプリのタイトルを設定
st.title("Image Swipe App")

# ページに説明を追加
st.write("Swipe left for dislike and right for like")

# 初期画面で表示される10枚の画像を取得
images = [get_random_image() for _ in range(10)]

# 画像を表示する要素を作成
image_container = st.empty()

# 画像をスワイプするための要素を作成
swipe_container = st.empty()

# ユーザーがスワイプした画像のインデックスを保持する変数を定義
liked_images = []

# 画像を表示し、ユーザーがスワイプする処理をループ
for i, image_url in enumerate(images):
    # 画像を取得
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # 画像を表示
    image_container.image(image, use_column_width=True)

    # ユーザーがスワイプした方向を取得
    direction = swipe_container.beta_columns(2)
    if direction[0].button("Dislike"):
        pass
    elif direction[1].button("Like"):
        liked_images.append(i)

# ユーザーがLIKEした画像を再表示
st.write("Liked images:")
for i in liked_images:
    response = requests.get(images[i])
    image = Image.open(BytesIO(response.content))
    st.image(image, use_column_width=True)

