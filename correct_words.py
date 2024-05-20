import re
import os

def correct_split_words(text, endings):
    pattern = r'\b(\w+) (' + '|'.join(endings) + r')\b'
    corrected_text = re.sub(pattern, r'\1\2', text)
    return corrected_text

folder_path = 'data_cleaned2'

specific_endings = [
    'ий', 'ої', 'ів', 'дь', 'ому', 'им', 'ть', 'ін', "єкт", "єрний", "ся", "апа", "відді", "утат", "ратив", "ькі", "викня", "мате", "ія", "мих", "івна", "онання", "етні", "відді", "титуція", "хко", "льно", "икий", "исала", "льно", "инула", "ожний", "утат", "уд", "лу", "ікати", "печити", "печення", "печимо", "’ям", "вний", "ити", "ати", "х", "ня", "ни", "му", "ла", "’ять", "мітету",
    # "", "", ""
    "ів",
    "равильно",
    "го",
    "ю",
    "им",
    "м",
    "ої",
    "юджет",
    "ньої",
    "ну",
    "нь",
    "’єднання",
    "и",
    "ється",
    "женні",
    "ю",
    "’являються",
    "акож",
    "ідно",
    "єю",
    "ього",
    "уватися",
    "ивну",
    "ння",
    "о",
    "вляється",
    "кт",
    "ими",
    "кту",
    "опроект",
    "ни",
    "же",
    "рошу",
    "ово",
    "ції",
    "овувати",
    "нутися",
    "ого",
    "ни",
    "татів",
    "ї",
    "ння",
    "осилення",
    "ьної",
    "ультатах",
    "одіваємося",
    "люваннях",

]
#specific_endings = ['зм']


changed_files = []

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        corrected_text = correct_split_words(text, specific_endings)
        
        if text != corrected_text:
            changed_files.append(filename)
            #breakpoint()
            corrected_file_path = os.path.join(folder_path, 'corrected')
            #with open(corrected_file_path, 'w', encoding='utf-8') as file:
            #    file.write(corrected_text)
            print(f"File changed and corrected: {filename}")
        else:
            continue
            print(f"No changes needed for: {filename}")

if changed_files:
    print("Files that were changed:", ', '.join(changed_files))
else:
    print("No files were changed.")
