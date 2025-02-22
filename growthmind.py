import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }  
    </style> 
    """,
    unsafe_allow_html=True
)

# Title with Icon 🚀
st.title("🛠️ DataSweeper Sterling Integrator by Sana Khalid")
st.write("🔄 Transform your file between CSV and Excel formats with built-in data cleaning and visualization.")

# File Uploader 📂
uploaded_files = st.file_uploader(
    "📥 Upload your file (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File Preview 🔍
        st.write(f"📄 **Preview of {file.name}**")
        st.dataframe(df.head())

        # Data Cleaning Options 🧼
        st.subheader(f"🛠️ Data Cleaning Options for {file.name}")

        if st.checkbox(f"✅ Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

            # Column Selection 🎯
            st.subheader("📌 Select Columns to Keep")
            columns = st.multiselect(f"🎯 Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data Visualization 📊
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"✅ Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options 🔄
        st.subheader("📂 File Conversion")
        conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📤 Convert & Download {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success("✅ File processed and ready for download!")
