import sys
import os
import pandas as pd
import streamlit as st

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from backend.data_cleaner import data_cleaner

# Set webpage title
st.title("📊 Data Cleaner")
st.write("Upload your raw CSV export below to clean it automatically.")

# Upload file
uploaded_file = st.file_uploader("Please select your file!", type=["csv"])

# Clean uploaded file
if uploaded_file is not None:
    st.success("File uploaded successfully!")

    clean_data = data_cleaner(uploaded_file)
    st.subheader("✨ Cleaned Data Preview")
    st.dataframe(clean_data.head(20))
