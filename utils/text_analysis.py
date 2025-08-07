import re
from collections import Counter
from nltk.corpus import stopwords

# Preload English stopwords set
STOPWORDS = set(stopwords.words('english'))

def clean_and_tokenize(text):
    # Lowercase, remove punctuation, split words
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def analyze_text(text):
    words = clean_and_tokenize(text)
    total_words = len(words)

    # Separate stopwords and nonstopwords
    stopword_list = [w for w in words if w in STOPWORDS]
    nonstopword_list = [w for w in words if w not in STOPWORDS]

    stopword_counts = Counter(stopword_list)
    nonstopword_counts = Counter(nonstopword_list)

    top_10_stopwords = stopword_counts.most_common(10)
    top_10_nonstopwords = nonstopword_counts.most_common(10)

    return {
        'total_words': total_words,
        'top_stopwords': top_10_stopwords,
        'top_nonstopwords': top_10_nonstopwords,
        'stopword_counts': stopword_counts,
        'nonstopword_counts': nonstopword_counts,
    }
