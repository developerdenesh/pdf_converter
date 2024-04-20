import streamlit as st
from pdf2docx import Converter
from io import BytesIO
import tabula
import pandas as pd

def checkType(type):
    if (type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        return "Excel"
    if (type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        return "Word"
    if (type == "application/pdf"):
        return "PDF"
    return "INVALID"

def pdf_to_excel(file, excel_file_path):
    # Read PDF file
    tables = tabula.read_pdf(file, pages='all')

    # Write each table to a separate sheet in the Excel file
    with pd.ExcelWriter(excel_file_path) as writer:
        for i, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f'Sheet{i+1}')


def main():
    st.title("File converter")
    st.write("Convert your pdfs to excel or word documents and vice versa")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        st.json({
            "filename": uploaded_file.name,
            "size": uploaded_file.size,
            "type": uploaded_file.type
        })
        type = checkType(uploaded_file.type)
        print(type)
        if (type == "Word"):
            pass
        elif (type == "Excel"):
            pass
        elif (type == "PDF"):
            answer = st.selectbox(
                'Select your preferred conversion',
                ('Select conversion','pdf to docx', 'pdf to xlsx')
            )
            if (answer == 'pdf to docx'):
                st.write(f"The option: {answer} has been chosen. Please wait for the conversion to take place")
                bytes_data = uploaded_file.getvalue()
                cv = Converter(stream=bytes_data)
                out_stream = BytesIO()
                cv.convert(out_stream)
                cv.close()
                # Download the file
                st.download_button(
                    label="Download file",
                    data=out_stream.getvalue(),
                    file_name="sample.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            elif (answer == 'pdf to xlsx'):
                st.write(f"The option: {answer} has been chosen. Please wait for the conversion to take place")
                with open("sample.pdf", 'wb') as f:
                    f.write(uploaded_file.getvalue())
                pdf_to_excel("sample.pdf", "sample.xlsx")
                with open('sample.xlsx', 'rb') as f:
                    st.download_button(
                        label='Download excel',
                        data=f,
                        file_name='sample.xlsx',
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )  # Defaults to 'application/octet-stream'
        else:
            st.error("This is an invalid file")
main()
