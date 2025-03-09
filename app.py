import streamlit as st
import pandas as pd
import numpy as np
import os as io

def clean_data(df, remove_duplicates=True, handle_missing="drop", remove_outliers=True):
    """Function to clean the dataset based on user selections"""
    
    # Remove duplicates
    if remove_duplicates:
        df = df.drop_duplicates()
    
    # Handle missing values
    if handle_missing == "drop":
        df = df.dropna()
    elif handle_missing == "fill_mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif handle_missing == "fill_median":
        df = df.fillna(df.median(numeric_only=True))
    
    # Remove outliers using IQR method
    if remove_outliers:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        Q1 = df[numeric_cols].quantile(0.25)
        Q3 = df[numeric_cols].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    
    return df

st.title("🧹 Data Sweeper App")
st.write("Upload your CSV file, clean it, and download the processed data!")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📂 Raw Data Preview")
    st.write(df.head())

    # Cleaning options
    remove_duplicates = st.checkbox("Remove Duplicates", value=True)
    handle_missing = st.selectbox("Handle Missing Values", ["drop", "fill_mean", "fill_median"])
    remove_outliers = st.checkbox("Remove Outliers (IQR Method)", value=True)

    if st.button("🧹 Clean Data"):
        cleaned_df = clean_data(df, remove_duplicates, handle_missing, remove_outliers)
        
        st.subheader("✅ Cleaned Data Preview")
        st.write(cleaned_df.head())

        # Convert DataFrame to CSV for download
        csv = cleaned_df.to_csv(index=False).encode()
        st.download_button("📥 Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")
