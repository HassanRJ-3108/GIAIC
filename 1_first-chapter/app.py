import streamlit as st
import pandas as pd
from io import BytesIO
import os
from xlsxwriter import Workbook
import re 

buffer = BytesIO()

st.set_page_config(page_title="Data Sweeper & Visualization",layout="wide", page_icon="🧹")
st.title("Data Sweeper & Visualization")
st.write("This is a simple tool to help you clean and visualize your data. You can upload a CSV file and perform various operations on it. You can also visualize the data using different types of plots.")

file = st.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'], accept_multiple_files=False)

if file:
    file_extension = os.path.splitext(file.name)[-1].lower()
    
    if file_extension == '.csv':
        df = pd.read_csv(file)
    elif file_extension == '.xlsx':
        df = pd.read_excel(file)
    else:
        st.write("Please upload a CSV or Excel file")
        st.stop()
    
    
    file_size_in_kb = len(file.getvalue()) / 1024
    st.write(f"**File Name**: {file.name}")
    st.write(f"**File size**: {file_size_in_kb:.2f} KB")
    
    
    
    st.subheader("View Data")
    st.write(df.head())
    
    st.subheader("Data Cleaning")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"Remove duplicates from {file.name} "):
            df = df.drop_duplicates()
            st.success("Duplicates removed successfully")
        
    with col2:
        if st.button(f"Remove Null values from {file.name}"):
            df = df.dropna()
            st.success("Null values removed successfully")
    
    
    
    st.subheader("Select columns to keep") 
    selected_columns = st.multiselect("Select columns to keep", df.columns, default=df.columns)
    if selected_columns:
        df = df[selected_columns]
        st.write(df.head())
    
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"Show Visualizations for {file.name}"):
            # First, check for numeric columns in the current dataframe
            numeric_cols = df.select_dtypes(include='number').columns

            if numeric_cols.empty:
                # Attempt to convert each column to numeric if possible
                converted_df = df.copy()
                for col in converted_df.columns:
                    converted_df[col] = pd.to_numeric(converted_df[col], errors='coerce')
                numeric_cols = converted_df.select_dtypes(include='number').columns

                if numeric_cols.empty:
                    st.warning("⚠️ No numeric columns available for visualization even after conversion.")
                else:
                    st.bar_chart(converted_df[numeric_cols].iloc[:, :2])
            else:
                st.bar_chart(df[numeric_cols].iloc[:, :2])        
    
    
      
    
    # File Conversion
    st.subheader("File Conversion")
    selected_type = st.radio("Select file type to convert", ['CSV', 'Excel'], key=file.name)
    if st.button(f"Convert your {file_extension} file to {selected_type}"):
        buffer = BytesIO()
        if selected_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_extension, ".csv")
            mine_type = "text/csv"
        else:
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            file_name = file.name.replace(file_extension, ".xlsx")
            mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        buffer.seek(0)
    
        st.download_button(
            label="Download the cleaned file of {} as {}".format(file.name, selected_type),
            data=buffer,
            file_name=file_name,
            mime=mine_type,
        )