import os

from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file_path):
    try:
        pdf_reader = PdfReader(pdf_file_path)
    except Exception as e:
        breakpoint()
    extracted_text = ""

    for page in pdf_reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

pdf_files_path = 'data_pdf/'
for pdf_file_name in os.listdir(pdf_files_path):
    if "data_pdf/.DS_Store" == pdf_files_path + pdf_file_name:
        continue
    extracted_text = extract_text_from_pdf(pdf_files_path + pdf_file_name)
    txt_file_path = 'data_txt/' + pdf_file_name.split(".pdf")[0] + ".txt"
    print(txt_file_path)

    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(extracted_text)

    print(f"Text extracted from {pdf_file_name} and saved in {txt_file_path}")
