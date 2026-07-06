import streamlit as st
from config.settings import APP_NAME

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Knowledge Assistant")

st.write("Welcome to the Enterprise RAG Application.")

st.success("Phase  Completed Successfully!")

from config.settings import OPENAI_API_KEY

if OPENAI_API_KEY:
    st.success("OpenAI API Key Loaded Successfully")
else:
    st.error("OpenAI API Key Not Found")