import spacy

from config import settings

# TODO: Сделать фильры по длительности фильма, по типу фильм-сериал и тд
# TODO: Отсылать на похожие фильмы


def text_analyse(text: str):
    filters = dict()
    filters["genres.name"] = []
    filters["typeNumber"] = []
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_stop and not token.is_punct]
    for token in tokens:
        if is_lemma_genre(token):
            filters["genres.name"].append(token.lemma_)
        if is_lemma_type(token):
            filters['typeNumber'].append(settings.TYPE_NUMBER_BY_TYPE_NAME[token.lemma_])
        elif is_lemma_year(token):
            filters["year"] = f"{token.nbor(-1).text}-{settings.CURRENT_YEAR}"
        elif is_lemma_rating(token):
            filters["rating.kp"] = f"{round(float(token.nbor(1).text), 0)}-{settings.MAX_KP_RATING}"
    return filters


def is_lemma_genre(token):
    if token.lemma_ in settings.GENRE_NAMES or token.text in settings.GENRE_NAMES:
        return True
    else:
        return False


def is_lemma_type(token):
    if token.lemma_ in settings.TYPE_NUMBER_BY_TYPE_NAME:
        return True
    else:
        return False


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
