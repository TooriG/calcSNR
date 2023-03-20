# -*- coding: utf-8 -*-

import streamlit as st
import random

def main():
    st.title("UNIQUE BETS")
    x = st.number_input("必要な額を入力してください。", min_value=0.01, step=0.01, value=1.00)
    y = st.number_input("賭ける額を入力してください。", min_value=0.01, step=0.01, value=1.00)
    
    if y >= x:
        st.warning("賭ける額は必要な額より小さくする必要があります。")
    else:
        if st.button("賭けを行う"):
            result = random.random()
            if result < y/x:
                st.success(f"{x}円を獲得しました！")
            else:
                st.warning("0円になりました(´；ω；`)")
        
if __name__ == '__main__':
    main()
