import os
import re

def clean_text(text :str) -> str:
    date_pattern = r'\(\w+, (\d+ \w+ \d{4} року)\)'
    #date = get_date(date_pattern, text[:80])
    #re.search(date_pattern, text[:80])
    text_without_content = re.sub(r'ЗМІСТ.*?\(\)', '', text, flags=re.DOTALL)
    text_without_first_word = re.sub(r'ЗМІСТ\s+', '', text_without_content, count=1)
    text_without_title = re.sub(r'Засідання [а-яА-Я\s,]+', '', text_without_first_word)
    text_without_anthem = re.sub(r'\(Лунає Державний Гімн України\)', '', text_without_title)
    text_without_applause = re.sub(r'\(Оплески\)', '', text_without_anthem)
    text_without_date = re.sub(r'\d{1,2} [а-я]+ \d{4} року', '', text_without_applause)

    return text_without_date#, date

def get_date(date_pattern, text):
    matches = re.search(date_pattern, text)

    if matches:
        date = matches.group(1)
        print(date)
    else:
        date = ""

    return date

txt_files_path = 'data_txt/'
for txt_file_name in os.listdir(txt_files_path):
    processed_text = []
    with open(os.path.join(txt_files_path, txt_file_name), 'r', encoding='utf-8') as file:
        text = file.read()
    cleaned_text = clean_text(text)

    txt_file_path = os.path.join('data_cleaned', txt_file_name)
    with open(txt_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)
