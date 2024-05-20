import os
import re

def fix_word_transfers_in_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    word_transfer_pattern = re.compile(r'(\w+)-\n(\w+)')
    fixed_text = re.sub(word_transfer_pattern, r'\1\2', text)

    fixed_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', fixed_text)

    with open(f'data_cleaned2/file_path', 'w', encoding='utf-8') as file:
        file.write(fixed_text)

files_path = 'data_cleaned/'
for file_name in os.listdir(files_path):
    fix_word_transfers_in_txt(file_name)
