import pandas as pd
import streamlit as st
from backend.data_cleaner import data_cleaner

# Set webpage title
st.title("📊 Data Cleaner")
st.write("Upload your raw CSV export below to clean it automatically.")

# Upload file
uploaded_file = st.file_uploader("Please select your file!", type=["csv"])

# Clean uploaded file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        clean_data = data_cleaner(df)
        st.subheader("✨ Cleaned Data Preview")
        st.dataframe(df.head(10))
    except Exception as e:
        st.error(f"An error occured: {e}")
