import os

folder_with_correct_names = 'data_processed'
folder_with_incorrect_names = 'data_processed2_cleaned'

correct_filenames = {}
for filename in os.listdir(folder_with_correct_names):
    identifier = filename.split('.')[0]
    correct_filenames[identifier] = filename

for incorrect_name in os.listdir(folder_with_incorrect_names):
    if 'None' in incorrect_name:
        identifier = incorrect_name.split('.')[0]
        correct_name = correct_filenames.get(identifier)
        if correct_name:
            current_path = os.path.join(folder_with_incorrect_names, incorrect_name)
            new_path = os.path.join(folder_with_incorrect_names, correct_name)
            
            os.rename(current_path, new_path)
            
            print(f"Renamed {incorrect_name} to {correct_name}")
        else:
            print(f"No match found for {incorrect_name}")
