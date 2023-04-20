import spacy
from config import settings


def text_analyse(text: str):
    filters = dict()
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    for token in doc:
        if is_lemma_genre(token):
            filters["genres.name"] = [token.lemma_]
        elif is_lemma_year(token):
            filters["year"] = f"{token.nbor(-1).text}-{settings.CURRENT_YEAR}"
        elif is_lemma_rating(token):
            filters["rating.kp"] = f"{round(float(token.nbor(1).text), 0)}-{settings.MAX_KP_RATING}"
    return filters


def is_lemma_genre(token):
    return True if token.lemma_ in settings.GENRE_NAMES else False


def is_lemma_year(token):
    if token.pos_ == "NOUN" and token.lemma_ in settings.YEAR_NAMES:
        if token.nbor(-1).pos_ == "NUM" or token.nbor(-1).pos_ == "ADJ":
            return True
    return False


def is_lemma_rating(token):
    if token.pos_ == "NOUN" and token.lemma_ in settings.RATING_NAMES:
        if token.nbor(1).pos_ == "NUM":
            return True
    return False
