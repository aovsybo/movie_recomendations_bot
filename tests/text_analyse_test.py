from unittest import TestCase, main

from config import settings
from services.text_analysis import text_analyse


class TextAnalyseRatingTest(TestCase):
    def test_start_end(self):
        message = "Хочу фильм с рейтингом от 3 до 6"
        rating = "3-6"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_start(self):
        message = "Посоветуй сериал 2012 года с оценкой выше 4"
        rating = f"4-{settings.MAX_KP_RATING}"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_end(self):
        message = "Какой сериал в жанре драма посмотреть с рейтингом меньше 9"
        rating = f"{settings.START_KP_RATING}-9"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_one_mark(self):
        message = "Комедия с оценкой 7"
        rating = "7-8"

        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_no_rating(self):
        message = "Сериал в жанре фантастика 2014 года"
        rating = f"{settings.START_KP_RATING}-{settings.MAX_KP_RATING}"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_no_keyword(self):
        message = "Мультфильм 2014 года 8 и выше"
        rating = f"{settings.START_KP_RATING}-{settings.MAX_KP_RATING}"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)

    def test_rating_out_of_range(self):
        message = "Аниме с рейтингом 23"
        rating = f"{settings.START_KP_RATING}-{settings.MAX_KP_RATING}"
        self.assertEqual(text_analyse(message)["rating.kp"], rating)


if __name__ == '__main__':
    main()
