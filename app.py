import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

st.set_page_config(page_title="Data Profiler", layout="wide")


def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb


def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in (".csv", ".xlsx"):
        return ext
    else:
        return False


# sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv, .xlsx files not exceeding 10 MB")
    if uploaded_file is not None:
        st.write("Mode of Operations")
        minimal = st.checkbox("Do you want summary report ?")
        st.markdown("*Summary report will work only in Primary Mode*")
        display_mode = st.radio("Display mode:", options=("Primary", "Dark", "Organge"))

        if display_mode == "Dark":
            dark_mode = True
            orange_mode = False
        elif display_mode == "Organge":
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        file_size = get_filesize(uploaded_file)
        if file_size <= 10:
            if ext == ".csv":
                # Load csv data
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox("Select the sheet", sheet_tuple)
                df = xl_file.parse(sheet_name=sheet_name)

            # Show dataframe
            # st.dataframe(df.head())

            # generate report
            with st.spinner("Generating report"):
                pr = ProfileReport(
                    df, minimal=minimal, dark_mode=dark_mode, orange_mode=orange_mode
                )

            st_profile_report(pr)
        else:
            st.error(
                "Maximum allowed file size is 10 MB. The current file uploaded has {file_size} MB"
            )
    else:
        st.error("Kindly upload only .csv or .xlsx file")
else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate profiling")
