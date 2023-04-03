# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# ページング用のパラメータ
page = 1
per_page = 10

# 検索ワードを取得
search_word = st.text_input("Search Images", "cat")

# 検索ボタンを押下した時の処理
if st.button("Search"):
    # APIから画像の情報を取得
    url = f"https://pixabay.com/api/?key="https://api.unsplash.com/photos/random?client_id=AbkbZ5qQ-hd5bzJ1nZ4NB7Ko8F6D8__ALTS0F8jXOko"&q={search_word}&image_type=photo&per_page={per_page}&page={page}"
    res = requests.get(url)
    data = res.json()
    
    # 取得した画像を表示
    for item in data['hits']:
        image_url = item['largeImageURL']
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=item['tags'], width=300)
    
    # ページング用のボタンを表示
    if data['totalHits'] > per_page:
        num_pages = data['totalHits'] // per_page
        if data['totalHits'] % per_page > 0:
            num_pages += 1
        page = st.slider("Page", 1, num_pages, 1)


