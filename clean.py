import re
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")
stop_words = set(stopwords.words("russian"))

habr_data = pd.read_csv('habr_articles.csv')
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|[^а-яА-Я\s]", " ", text)
    words = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return words

habr_data = pd.read_csv('habr_articles.csv')
all_summaries = ' '.join(habr_data['Summary'].astype(str))
cleaned_words = clean_text(all_summaries)

word_counts = Counter(cleaned_words)
most_common_words = word_counts.most_common(20)

words, frequencies = zip(*most_common_words)
plt.figure(figsize=(12, 6))
plt.bar(words, frequencies, color='skyblue')
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("Top 20 Most Common Words in Habr Articles Summary")
plt.xticks(rotation=45)
plt.show()

wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Habr Articles Summary")
plt.show()

print(most_common_words)
russian_stop_words = {
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", "все", "она",
    "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по", "только", "ее",
    "мне", "было", "вот", "от", "меня", "еще", "нет", "о", "из", "ему", "теперь", "когда",
    "даже", "ну", "вдруг", "ли", "если", "уже", "или", "ни", "быть", "был", "него", "до",
    "вас", "нибудь", "опять", "уж", "вам", "ведь", "там", "потом", "себя", "ничего", "ей",
    "может", "они", "тут", "где", "есть", "надо", "ней", "для", "мы", "тебя", "их", "чем",
    "была", "сам", "чтоб", "без", "будто", "чего", "раз", "тоже", "себе", "под", "будет",
    "ж", "тогда", "кто", "этот", "того", "потому", "этого", "какой", "совсем", "ним",
    "здесь", "этом", "один", "почти", "мой", "тем", "чтобы", "нее", "сейчас", "были",
    "куда", "зачем", "всех", "никогда", "можно", "при", "наконец", "два", "об", "другой",
    "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про", "всего",
    "них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою",
    "этой", "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой", "им", "более",
    "всегда", "конечно", "всю", "между"
}

def clean_text_with_manual_stopwords(text):
    text = text.lower()
    text = re.sub(r"http\S+|[^а-яА-Я\s]", " ", text)
    words = [word for word in text.split() if word not in russian_stop_words and len(word) > 2]
    return words

all_summaries = ' '.join(habr_data['Summary'].astype(str))

cleaned_words_manual = clean_text_with_manual_stopwords(all_summaries)

word_counts_manual = Counter(cleaned_words_manual)
most_common_words_manual = word_counts_manual.most_common(20)

words, frequencies = zip(*most_common_words_manual)
plt.figure(figsize=(12, 6))
plt.bar(words, frequencies, color='skyblue')
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("Top 20 Most Common Words in Habr Articles Summary (Manual Stop Words)")
plt.xticks(rotation=45)
plt.show()

wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_counts_manual)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Habr Articles Summary (Manual Stop Words)")
plt.show()

print(most_common_words_manual)