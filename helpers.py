import os
import string

import gensim
from gensim import corpora
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import spacy

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('vader_lexicon')

stop = set(stopwords.words('german'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
nlp = spacy.load("uk_core_news_sm")

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def preprocess(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop]
    return lemmatized

def read_file(file_name):
    with open(os.path.join("data_processed", file_name), 'r', encoding='utf-8') as file:
        text = file.read()
    return text