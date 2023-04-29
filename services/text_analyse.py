import spacy

from config import settings


def text_analyse(text: str):
    filters = {
        "genres.name": [],
        "typeNumber": [],
        "year": f"{settings.START_SEARCH_FROM_YEAR}-{settings.CURRENT_YEAR}",
        "rating.kp": f"{settings.START_KP_RATING}-{settings.MAX_KP_RATING}",
    }
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
            filters['year'] = format_year_string(token, filters['year'])
        elif is_lemma_rating(token) and has_rating_words([t.lemma_ for t in doc if not t.is_punct]):
            filters["rating.kp"] = format_rating_string(token, filters["rating.kp"])
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
            if settings.MIN_YEAR <= num <= settings.CURRENT_YEAR:
                return True
    return False


def is_lemma_rating(token):
    if token.pos_ == "NUM"  and len(token.text) in (1, 2):
        try:
            num = int(token.text)
        except ValueError:
            return False
        else:
            if settings.MIN_KP_RATING <= num <= settings.MAX_KP_RATING:
                return True
    return False


def has_words_before(token, word_list: list[str]):
    try:
        text_before = token.nbor(-1).text
    except IndexError:
        return False
    else:
        if text_before in word_list:
            return True
        else:
            return False


def format_year_string(token, current_year):
    """Если лемма является годом (1900-н.в.), то проверяем, это начало или конец диапазона,
    либо конкретный год без диапазона (тогда он и начало, и конец),
    и в зависимости от этого подставляем год в ту или иную позицию
    чтобы получить диапазон в формате "year_start-year_end"""
    checking_year = int(token.text)
    if has_words_before(token, settings.YEAR_UNTIL_WORDS):
        if checking_year < int(current_year[0:4]):
            return f"{settings.MIN_YEAR}-{checking_year}"
        return f"{current_year[0:4]}-{checking_year}"
    elif has_words_before(token, settings.YEAR_FROM_WORDS):
        if checking_year > int(current_year[5:9]):
            return f"{settings.MIN_YEAR}-{current_year[5:9]}"
        return f"{checking_year}-{current_year[5:9]}"
    else:
        return f"{token.text}-{token.text}"


def format_rating_string(token, current_rating):
    checking_rating = int(token.text)
    if has_words_before(token, settings.RATING_UNTIL_WORDS):
        return f"{current_rating[0:1]}-{checking_rating}"
    elif has_words_before(token, settings.RATING_FROM_WORDS):
        return f"{checking_rating}-{current_rating[2:]}"
    else:
        return f"{checking_rating}-{checking_rating+1}"


def has_rating_words(tokens):
    return True if set(tokens).intersection(set(settings.RATING_WORDS)) else False