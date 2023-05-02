import spacy

from config import settings


def text_analyse(text: str):
    filters = init_filters()
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
            filters['year'] = format_string_for_request(
                token,
                filters['year'],
                int,
                settings.YEAR_FROM_WORDS,
                settings.YEAR_UNTIL_WORDS,
                settings.MIN_YEAR
            )
        elif is_lemma_rating(token) and has_rating_words([t.lemma_ for t in doc if not t.is_punct]):
            filters["rating.kp"] = format_string_for_request(
                token,
                filters["rating.kp"],
                float,
                settings.RATING_FROM_WORDS,
                settings.RATING_UNTIL_WORDS,
                settings.MIN_KP_RATING
            )
    return filters


def init_filters():
    return {
        "genres.name": [],
        "typeNumber": [],
        "year": f"{settings.START_SEARCH_FROM_YEAR}-{settings.CURRENT_YEAR}",
        "rating.kp": f"{settings.START_KP_RATING}-{settings.MAX_KP_RATING}",
    }


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
    if token.pos_ == "NUM":
        try:
            num = float(token.text)
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


def format_string_for_request(token, current_value, current_type, from_words, until_words, min_value):
    """Если лемма является годом (1900-н.в.), то проверяем, это начало или конец диапазона,
    либо конкретный год без диапазона (тогда он и начало, и конец),
    и в зависимости от этого подставляем год в ту или иную позицию
    чтобы получить диапазон в формате "year_start-year_end. Аналогично с рейтингом"""
    checking_value = current_type(token.text)
    current_start_value, current_end_value = current_value.split('-')
    if has_words_before(token, until_words):
        if checking_value < current_type(current_start_value):
            return f"{min_value}-{checking_value}"
        return f"{current_start_value}-{checking_value}"
    elif has_words_before(token, from_words):
        if checking_value > current_type(current_end_value):
            return f"{min_value}-{current_end_value}"
        return f"{checking_value}-{current_end_value}"
    else:
        # В случае, если нужен фильм с конкретным годом, бдует поиск в диапазоне год..год
        # А с рейтингом будет рейтинг..рейтинг+0.9, чтобы расширить диапазон поиска по рейтингу
        return f"{checking_value}-{current_type(checking_value+0.9)}"


def has_rating_words(tokens):
    return True if set(tokens).intersection(set(settings.RATING_WORDS)) else False