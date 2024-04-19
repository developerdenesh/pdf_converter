import streamlit as st
from pdf2docx import Converter
from io import BytesIO

def main():
    st.write("hello world")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        st.write(f"filename: {uploaded_file.name}, size: {uploaded_file.size}")
        bytes_data = uploaded_file.getvalue()
        cv = Converter(stream=bytes_data)
        out_stream = BytesIO()
        cv.convert(out_stream)
        cv.close()
        # Download the file
        btn = st.download_button(
            label="Download file",
            data=out_stream.getvalue(),
            file_name="sample.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

main()
