import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page


page = st.sidebar.selectbox("Menu", ("Prediksi Gaji Kamu", "Informasi Data"))

if page == "Prediksi Gaji Kamu":
    show_predict_page()
else:
    show_explore_page()