import spacy
from config import settings


def text_analyse(text: str):
    filters = dict()
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    for token in doc:
        if token.lemma_ in settings.GENRE_NAMES:
            filters["genres.name"] = [token.lemma_]
        elif token.pos_ == "NOUN" and token.lemma_ in settings.YEAR_NAMES:
            prev_token = token.nbor(-1)
            if prev_token.pos_ == "NUM" or prev_token.pos_ == "ADJ":
                filters["year"] = f"{prev_token.text}-{settings.CURRENT_YEAR}"
        elif token.pos_ == "NOUN" and token.lemma_ in settings.RATING_NAMES:
            next_token = token.nbor(1)
            if next_token.pos_ == "NUM":
                filters["rating.kp"] = f"{round(float(next_token.text), 0)}-{settings.MAX_KP_RATING}"
    return filters
