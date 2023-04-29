import spacy

from config import settings


def text_analyse(text: str):
    filters = dict()
    filters["genres.name"] = []
    filters["typeNumber"] = []
    filters["year"] = f"{settings.START_SEARCH_FROM_YEAR}-{settings.CURRENT_YEAR}"
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_punct]
    for token in tokens:
        if is_lemma_genre(token):
            filters["genres.name"].append(token.lemma_)
        elif is_text_genre(token):
            filters["genres.name"].append(token.text)
        if is_lemma_type(token):
            filters['typeNumber'].append(settings.TYPE_NUMBER_BY_TYPE_NAME[token.lemma_])
        elif is_lemma_year(token):
            # Если лемма является годом, то проверяем, это год начала поиска, или конца поиска,
            # или нужен фильм конкретного года (тогда год и начала, и конца),
            # и в зависимости от этого подставляем год в ту или иную позицию
            # чтобы получить диапазон в формате "year_start-year_end"
            year = int(token.text)
            if has_words_before_year(token, settings.YEAR_UNTIL_WORDS):
                filters['year'] = f"{filters['year'][0:4]}-{year}"
            elif has_words_before_year(token, settings.YEAR_FROM_WORDS):
                filters['year'] = f"{year}-{filters['year'][5:9]}"
            else:
                filters["year"] = f"{token.text}-{token.text}"
        elif is_lemma_rating(token):
            filters["rating.kp"] = f"{round(float(token.nbor(1).text), 0)}-{settings.MAX_KP_RATING}"
    return filters


def is_lemma_genre(token):
    if token.lemma_ in settings.GENRE_NAMES:
        return True
    else:
        return False


def is_text_genre(token):
    if token.text in settings.GENRE_NAMES:
        return True
    else:
        return False


def is_lemma_type(token):
    if token.lemma_ in settings.TYPE_NUMBER_BY_TYPE_NAME:
        return True
    else:
        return False


def is_lemma_year(token):
    if (token.pos_ == "ADJ" or token.pos_ == "NUM") and len(token.text) == 4:
        try:
            num = int(token.text)
        except ValueError:
            return False
        else:
            if 1900 <= num <= settings.CURRENT_YEAR:
                return True
    return False


def has_words_before_year(token, word_list: list[str]):
    try:
        text_before = token.nbor(-1).text
    except IndexError:
        return False
    else:
        if text_before in word_list:
            return True
        else:
            return False


def is_lemma_rating(token):
    if token.pos_ == "NOUN" and token.lemma_ in settings.RATING_NAMES:
        try:
            if token.nbor(1).pos_ == "NUM":
                return True
        except IndexError:
            return False
    return False
