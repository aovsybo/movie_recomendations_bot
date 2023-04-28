import spacy

from config import settings


def text_analyse(text: str):
    filters = dict()
    filters["genres.name"] = []
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_stop and not token.is_punct]
    for token in tokens:
        if is_lemma_genre(token):
            filters["genres.name"].append(token.lemma_)
        elif is_lemma_year(token):
            filters["year"] = f"{token.nbor(-1).text}-{settings.CURRENT_YEAR}"
        elif is_lemma_rating(token):
            filters["rating.kp"] = f"{round(float(token.nbor(1).text), 0)}-{settings.MAX_KP_RATING}"
    return filters


def is_lemma_genre(token):
    return True if token.lemma_ in settings.GENRE_NAMES else False


def is_lemma_year(token):
    if token.pos_ == "NOUN" and token.lemma_ in settings.YEAR_NAMES:
        try:
            if token.nbor(-1).pos_ == "NUM" or token.nbor(-1).pos_ == "ADJ":
                return True
        except IndexError:
            return False
    return False


def is_lemma_rating(token):
    if token.pos_ == "NOUN" and token.lemma_ in settings.RATING_NAMES:
        try:
            if token.nbor(1).pos_ == "NUM":
                return True
        except IndexError:
            return False
    return False
