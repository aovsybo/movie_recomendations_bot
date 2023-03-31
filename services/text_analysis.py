import spacy


genre_names = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых',
               'документальный', 'драма', 'игра', 'история', 'комедия', 'концерт', 'короткометражка',
               'криминал', 'мелодрама', 'музыка', 'мультфильм', 'мюзикл', 'новости', 'приключения',
               'реальное ТВ', 'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар',
               'фэнтези', 'церемония']
rating_names = ["оценка", "рейтинг"]
year_names = ["год"]


def text_analyse(text: str):
    filters = dict()
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    for token in doc:
        if (token.pos_ == "NOUN" or token.pos_ in "ADJ") and token.lemma_ in genre_names:
            filters["genres.name"] = [token.lemma_]
        elif token.pos_ == "NOUN" and token.lemma_ in year_names:
            prev_token = token.nbor(-1)
            if prev_token.pos_ == "NUM" or prev_token.pos_ == "ADJ":
                filters["year"] = f"{prev_token.text}-2023"
                # filters["year"] = f"{prev_token.text}"
        elif token.pos_ == "NOUN" and token.lemma_ in rating_names:
            next_token = token.nbor(1)
            if next_token.pos_ == "NUM":
                filters["rating.kp"] = f"{next_token.text}-10"
                # filters["rating.kp"] = f"{next_token.text}"
    return filters
