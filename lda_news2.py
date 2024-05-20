import os
import gensim
from gensim import corpora
import spacy
import pandas as pd
import json

# Initialize NLP tools
print("Initializing NLP tools...")
nlp = spacy.load("uk_core_news_sm")
stopwords_ua = pd.read_csv("stopwords_ua_news.txt", header=None, names=['stopwords']).stopwords.tolist()

input_dir = "data_processed_news"
period_definitions = {
    'winter': ['12', '01'],
    'spring': ['02', '03', '04', '05'],
    'summer': ['06', '07', '08', '09'],
    'autumn': ['10', '11']
}

def preprocess(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.lemma_ not in stopwords_ua]

def create_dictionary(year, period):
    print(f"Creating dictionary from news data for year {year}, period {period}...")
    texts = []
    for filename in os.listdir(input_dir):
        if year in filename:
            date_part = filename.split('_')[1]
            month, file_year = date_part.split('-')[1], date_part.split('-')[0]
            if month in period_definitions[period] and int(file_year) == int(year):
                print(f"Processing file: {filename}")
                with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    processed_text = preprocess(text)
                    texts.append(processed_text)
    dictionary = corpora.Dictionary(texts)
    dictionary_path = f'generated_dictionary_{year}_{period}.dict'
    dictionary.save(dictionary_path)
    print(f"Dictionary created and saved as '{dictionary_path}'.")
    return dictionary, dictionary_path

def load_or_create_dictionary(year, period):
    dictionary_path = f'generated_dictionary_{year}_{period}.dict'
    if os.path.exists(dictionary_path):
        print(f"Loading existing dictionary for year {year}, period {period}...")
        dictionary = corpora.Dictionary.load(dictionary_path)
    else:
        dictionary, _ = create_dictionary(year, period)
    return dictionary

def process_files(year):
    print(f"Processing files for year {year}...")
    texts_by_period = {period: [] for period in period_definitions}
    for filename in os.listdir(input_dir):
        if year in filename:
            date_part = filename.split('_')[1]
            month, file_year = date_part.split('-')[1], date_part.split('-')[0]
            for period, months in period_definitions.items():
                if month in months and int(file_year) == int(year):
                    filepath = os.path.join(input_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        text = [line.split(',')[1].strip() for line in file if line.strip() and line.split(',')[1].strip() not in stopwords_ua]
                    processed_text = preprocess(' '.join(text))
                    texts_by_period[period].append(processed_text)
                    print(f"Processed file: {filename} for period: {period}")
    return texts_by_period

def get_topics_for_new_documents(texts_by_period, year):
    topics_by_period = {}
    for period, texts in texts_by_period.items():
        if not texts:
            print(f"No texts found for {period}.")
            continue
        dictionary = load_or_create_dictionary(year, period)
        print(f"Loading LDA model for period: {period} in year: {year}...")
        model_path = f'{year}/lda_{period}_{year}.model'
        lda_model = gensim.models.LdaModel.load(model_path)
        corpus = [dictionary.doc2bow(text) for text in texts]

        topic_word_counts = {}
        for bow in corpus:
            doc_topics = lda_model.get_document_topics(bow)
            for topic_id, topic_prob in doc_topics:
                if topic_id not in topic_word_counts:
                    topic_word_counts[topic_id] = {}
                for word_id, count in bow:
                    word = dictionary[word_id]
                    if word in topic_word_counts[topic_id]:
                        topic_word_counts[topic_id][word] += count * topic_prob
                    else:
                        topic_word_counts[topic_id][word] = count * topic_prob

        topic_words = {}
        for topic_id, word_counts in topic_word_counts.items():
            sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:25]
            topic_words[f'topic_{topic_id+1}'] = [word for word, count in sorted_words]

        topics_by_period[period] = topic_words
        print(f"Generated topics for period: {period} in year: {year}")
    return topics_by_period

def save_topics_to_json(topics_by_period, year):
    output_dir = os.path.join(str(year), "news")
    os.makedirs(output_dir, exist_ok=True)    
    for period, topics in topics_by_period.items():
        with open(os.path.join(output_dir, f'topics_{period}_{year}.json'), 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=4)
        print(f"Saved topics to {output_dir}/topics_{period}_{year}.json")

year = "2023"
texts_by_period = process_files(year)
for period in texts_by_period:
    print(f"\nProcessing {period} of {year}")
    topics_by_period = get_topics_for_new_documents(texts_by_period, year)
save_topics_to_json(topics_by_period, year)
print("Topics saved to JSON files.")
