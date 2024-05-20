import os
import string
from collections import Counter
import plotly.graph_objects as go


folder_path = 'data_cleaned2'

stopwords_file = 'stopwords_ua.txt'

with open(stopwords_file, 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

word_counter = Counter()
punctuation = string.punctuation + "“" + "”" + "—" + "№" + "–" + "’" + "»"

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
            words = [word.strip(punctuation).lower() for word in words if word.strip(string.punctuation).lower() not in stopwords]
            words = [word for word in words if word]
            word_counter.update(words)

total_words = sum(word_counter.values())
print("Загальна кількість слів:", total_words)

unique_words = len(word_counter)
print("Кількість унікальних слів:", unique_words)

lemma_counter = Counter()
folder_path = 'data_processed2_cleaned'
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                lemma = line.strip(punctuation).lower()
                if lemma not in stopwords:
                    lemma_counter.update([lemma])

total_words = sum(lemma_counter.values())
print("Загальна кількість лем:", total_words)

unique_words = len(lemma_counter)
print("Кількість унікальних лем:", unique_words)
breakpoint()

top_10_words = word_counter.most_common(10)
print("Топ-10 слів:")
for word, count in top_10_words:
    print(f"{word}: {count}")

words, counts = zip(*top_10_words)

fig = go.Figure(data=[go.Bar(x=words, y=counts)])
fig.update_layout(title='TOP 10 Words', xaxis_title='Word', yaxis_title='Amount')
fig.write_image("top_10_words.png")

top_10_words = lemma_counter.most_common(10)
print("Топ-10 лем:")
for word, count in top_10_words:
    print(f"{word}: {count}")

words, counts = zip(*top_10_words)

fig = go.Figure(data=[go.Bar(x=words, y=counts)])
fig.update_layout(title='TOP 10 Lemmas', xaxis_title='Lemma', yaxis_title='Amount')
fig.write_image("top_10_lemmas.png")
