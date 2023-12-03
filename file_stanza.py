import csv
import os
import string
import re

from datetime import datetime

import stanza


stanza.download('uk')
nlp = stanza.Pipeline('uk', processors='tokenize,lemma')

# name entity recognition of date
# parse date
# remove pages and "..." +
# remove all punctuation - +
# create github repository
# stemming later
# gamcing for LDA later

month_map = {
    "січня": 1, "лютого": 2, "березня": 3, "квітня": 4, "травня": 5, "червня": 6,
    "липня": 7, "серпня": 8, "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
}
ignored_list = [
    "(Після перерви)",
    "(Шум у залі) .",
    "(Хвилина мовчання) .",
    "(Середа, )",
    "(Не чути) .",
    "(Шум у залі)  Увага, без шуму!",
    "(Хвилина мовчання)"
]

def contains_only_punctuation(text):
    return bool(re.match(f"[{string.punctuation}]+$", text))

def get_date(splitted_elements):
    
    try:
        if len(splitted_elements) == 6:
            day, month_name, year = splitted_elements[2:5]
        else:
            day, month_name, year = splitted_elements[1:4]
        month = month_map[month_name]
    except Exception as e:
        return None, None, None

    parsed_date = datetime(int(year), month, int(day))
    day = parsed_date.day
    month = parsed_date.month
    year = parsed_date.year

    return day, month, year

txt_files_path = 'data_cleaned/'
for txt_file_name in os.listdir(txt_files_path):
    print(txt_file_name)
    processed_text = []
    with open(os.path.join(txt_files_path, txt_file_name), 'r', encoding='utf-8') as file:
        text = file.read()

    doc = nlp(text)

    parse_date_flag = True
    for sentence in doc.sentences:
        if parse_date_flag and sentence.text.startswith("(") and sentence.text not in ignored_list and "Шум" not in sentence.text:
            splitted_elements = sentence.text.split()
            if len(splitted_elements) > 3:
                print(sentence.text)
                day, month, year = get_date(splitted_elements)
                if day:
                    parse_date_flag = False

        for token in sentence.tokens:
            processed_text.append((token.text, token.words[0].lemma))

    txt_file_path = os.path.join(f'data_processed', txt_file_name.split("txt")[0] + f'{day}_{month}_{year}' + '.txt')
    print(txt_file_path)
    with open(txt_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for sentence in doc.sentences:
            for token in sentence.tokens:
                if not contains_only_punctuation(token.text) and token.text != "…" and token.text != "«" and token.text != "»" and token.text != "–":
                    csv_writer.writerow([token.text, token.words[0].lemma])
