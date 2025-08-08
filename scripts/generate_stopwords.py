import spacy

def main():
    nlp = spacy.load("en_core_web_sm")
    stopwords = sorted(nlp.Defaults.stop_words)

    with open("data/spacy_stopwords.py", "w", encoding="utf-8") as f:
        f.write("# Auto-generated stopwords list from SpaCy\n")
        f.write("STOPWORDS = {\n")
        for word in stopwords:
            f.write(f"    {word!r},\n")
        f.write("}\n")

if __name__ == "__main__":
    main()
