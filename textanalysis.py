import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

st.title("特徴的な単語の順位を出力するアプリ")

# ユーザーが入力したテキストを取得
user_input = st.text_area("テキストを入力してください", "")

if user_input:
    # テキストを前処理
    preprocessed_text = user_input.lower().replace("\n", " ")

    # TF-IDFによる特徴的な単語の抽出
    vectorizer = TfidfVectorizer(stop_words="english")
    tf_idf = vectorizer.fit_transform([preprocessed_text])
    features = vectorizer.get_feature_names()

    # 特徴的な単語の重要度を計算
    word_scores = pd.DataFrame(
        tf_idf.T.todense(),
        index=features,
        columns=["score"]
    )
    word_scores = word_scores.sort_values(by="score", ascending=False)

    # 結果を表示
    st.write("入力されたテキストから特徴的な単語の順位：")
    for i, word in enumerate(word_scores.index):
        st.write(f"{i+1}. {word}")
