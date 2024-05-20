import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

folder_path = 'data_processed2_cleaned'

corpus = []
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            corpus.append(file.read())

tfidf_vectorizer = TfidfVectorizer()

tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

average_tfidf_scores = np.mean(tfidf_matrix.toarray(), axis=0)

feature_names = tfidf_vectorizer.get_feature_names_out()

word_tfidf_dict = dict(zip(feature_names, average_tfidf_scores))

sorted_word_tfidf = sorted(word_tfidf_dict.items(), key=lambda x: x[1])

print("Words with lowest TF-IDF scores (potential stoplist candidates):")
#for word, score in sorted_word_tfidf[-50:]:
for word, score in sorted_word_tfidf[-100:-50]:
    print(word)
    #print(f"{word}: {score}")
