import os
import json
import numpy as np
import string
import gensim
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
import pandas as pd
import pyLDAvis.gensim
import pyLDAvis
import plotly.express as px

from utils import timing

nlp = spacy.load("uk_core_news_sm")
stopwords_ua = pd.read_csv("stopwords_ua.txt", header=None, names=['stopwords'])
stop_words_ua = list(stopwords_ua.stopwords)
lemma = WordNetLemmatizer()

NUM_OF_TOPICS = {
    'winter': 7,
    'spring': 22,
    'summer': 25,
    'autumn': 24,
}

def clean(doc):
    punctuation = string.punctuation + "“" + "”" + "—" + "№" + "–" + "’"
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop_words_ua])
    punc_free = "".join([word for word in stop_free if word not in punctuation])
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def preprocess(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and token.lemma_ not in stop_words_ua]
    return lemmatized

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.replace('\n', ' ')
    cleaned_text = clean(text)
    return preprocess(cleaned_text)

input_dir = "data_processed2_cleaned"
texts_by_year = {}

def get_texts(year):
    period_definitions = {
        'winter': ['12', '01'],
        'summer': ['06', '07', '08', '09'],
        'autumn': ['10', '11'],
        'spring': ['02', '03', '04', '05'],
    }
    texts_by_period = {period: [] for period in period_definitions}
    for file_name in os.listdir(input_dir):
        if year not in file_name:
            continue
        month = file_name.split('_')[1].split('.')[0]

        for period, months in period_definitions.items():
            if month in months:
                file_path = os.path.join(input_dir, file_name)
                processed_text = process_file(file_path)
                texts_by_period[period].append(processed_text)
                break
    return texts_by_period

@timing
def get_coherance(model, texts, dictionary):
    coherence_model_lda = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v', topn=20)
    coherance_score = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherance_score)
    per_topic = coherence_model_lda.get_coherence_per_topic()
    print("per_topic: ", per_topic)
    return coherance_score


if __name__ == '__main__':
    years = ["2017"]
    for year in years:
        texts_by_year = get_texts(year)
        finding_best_topics_amount = False

        # Обробляємо тексти за кожним роком
        for period, texts in texts_by_year.items():
            dictionary = corpora.Dictionary(texts)
            corpus = [dictionary.doc2bow(text) for text in texts]
            results = []
            if finding_best_topics_amount:
                for topics_amount in range(2, 51):
                    lda = gensim.models.LdaMulticore(corpus=corpus,
                        id2word=dictionary,
                        chunksize=100000,
                        num_topics=10,
                        passes=20,
                        workers=1,
                        iterations=10000
                    )
                    print(f'\nPerplexity for {topics_amount} topics: {lda.log_perplexity(corpus)}')
                    coherence_score = get_coherance(lda, texts, dictionary)
                    results.append((topics_amount, coherence_score))

                df = pd.DataFrame(results, columns=['Number of Topics', 'Coherence Score'])

                fig = px.line(df, x='Number of Topics', y='Coherence Score', markers=True, title=f'Coherence Score by Number of Topics for {period} {year}')
                fig.update_layout(xaxis_title='Number of Topics', yaxis_title='Coherence Score', xaxis=dict(tickmode='array', tickvals=df['Number of Topics']))
                fig.update_yaxes(range=[0, 0.7])
                fig.show()
            else:
                topics_amount = NUM_OF_TOPICS.get(period)
                print(topics_amount)
                if topics_amount:
                    lda = gensim.models.LdaMulticore(corpus=corpus,
                        id2word=dictionary,
                        chunksize=100000,
                        num_topics=topics_amount,
                        passes=20,
                        workers=1,
                        iterations=10000
                    )
                    visualisation = pyLDAvis.gensim.prepare(lda, corpus, dictionary, R=15, mds='mmds')
                    print("saving...")
                    lda.save(f'{year}/lda_{period}_{year}.model')
                    topics = lda.show_topics(num_topics=25, num_words=25, formatted=False)
                    topics_dict = {
                        f'topic_{topic_id + 1}': [word for word, _ in words]
                        for topic_id, (_, words) in enumerate(topics)
                    }
                    with open(f'{year}/topics_{period}_{year}.json', 'w', encoding='utf-8') as f:
                        json.dump(topics_dict, f, ensure_ascii=False, indent=4)
                    pyLDAvis.save_html(visualisation, f'{year}/LDA_Visualization_{period}_{year}.html')
            print(f"Теми за {period} {year} рік:")
            topics = lda.print_topics(num_words=30)#50
            for topic in topics:
                continue
            print("\n" + "#" * 50 + "\n")
