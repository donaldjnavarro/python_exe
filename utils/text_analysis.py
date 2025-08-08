import re
from collections import Counter
from data.spacy_stopwords import STOPWORDS

def clean_and_tokenize(text):
    """
    Tokenize text by splitting on whitespace, then remove leading/trailing punctuation
    but keep internal apostrophes (contractions) intact.
    """
    tokens = text.lower().split()
    cleaned_tokens = []
    for token in tokens:
        # Remove leading/trailing punctuation (but not internal apostrophes)
        cleaned = re.sub(r"(^[^\w']+|[^\w']+$)", '', token)
        if cleaned:
            cleaned_tokens.append(cleaned)
    return cleaned_tokens

def is_all_stopwords(ngram, stopwords_set):
    return all(word in stopwords_set for word in ngram)

def get_filtered_ngrams(words, n, stopwords_set):
    ngrams = zip(*[words[i:] for i in range(n)])
    filtered = [ngram for ngram in ngrams if not is_all_stopwords(ngram, stopwords_set)]
    return filtered

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

    # Bigrams and trigrams with filtering
    bigrams = get_filtered_ngrams(words, 2, STOPWORDS)
    trigrams = get_filtered_ngrams(words, 3, STOPWORDS)

    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)

    top_bigrams = bigram_counts.most_common(10)
    top_trigrams = trigram_counts.most_common(10)

    # Format n-grams as strings for UI
    top_bigrams = [(" ".join(b), c) for b, c in top_bigrams]
    top_trigrams = [(" ".join(t), c) for t, c in top_trigrams]

    return {
        'total_words': total_words,
        'top_stopwords': top_10_stopwords,
        'top_nonstopwords': top_10_nonstopwords,
        'stopword_counts': stopword_counts,
        'nonstopword_counts': nonstopword_counts,
        'top_bigrams': top_bigrams,
        'top_trigrams': top_trigrams,
    }
