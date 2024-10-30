import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import Word2Vec, FastText
from sklearn.metrics import silhouette_score
from nltk.corpus import stopwords
import re

data = pd.read_csv('habr_articles.csv')
stop_words = set(stopwords.words('russian'))

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    tokens = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return ' '.join(tokens)

data['cleaned_summary'] = data['Summary'].apply(preprocess_text)

tfidf_vectorizer = TfidfVectorizer(max_df=0.85, min_df=2, ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform(data['cleaned_summary'])

tokenized_texts = [text.split() for text in data['cleaned_summary']]
w2v_model = Word2Vec(sentences=tokenized_texts, vector_size=100, window=5, min_count=2, sg=1)

def vectorize_with_tfidf(text):
    words = text.split()
    tfidf_weights = dict(zip(tfidf_vectorizer.get_feature_names_out(), tfidf_matrix.toarray().sum(axis=0)))
    vector = sum(w2v_model.wv[word] * tfidf_weights.get(word, 0) for word in words if word in w2v_model.wv)
    return vector / len(words)

data['tfidf_w2v'] = data['cleaned_summary'].apply(vectorize_with_tfidf)

sse = []
K = range(1, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=0).fit(list(data['tfidf_w2v'].dropna()))
    sse.append(kmeans.inertia_)

plt.plot(K, sse, 'bx-')
plt.xlabel('Число кластеров k')
plt.ylabel('Sum of squared distances')
plt.title('Метод локтя для оптимального k')
plt.show()

optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=0)
data['cluster'] = kmeans.fit_predict(list(data['tfidf_w2v'].dropna()))

pca = PCA(n_components=2)
reduced_data = pca.fit_transform(list(data['tfidf_w2v'].dropna()))

plt.figure(figsize=(10, 8))
for i in range(optimal_k):
    plt.scatter(reduced_data[data['cluster'] == i, 0], reduced_data[data['cluster'] == i, 1], label=f'Cluster {i}')
plt.legend()
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Тексты, распределенные по кластерам с помощью K-means')
plt.show()