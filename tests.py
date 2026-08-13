import pytest

from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


class TestBooksCollector:

    genres = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']

    # 1. При создании объекта в списке genre содержатся все доступные жанры
    @pytest.mark.parametrize('genre', genres)
    def test_init_genre_list_contains_all_genres(self, collector, genre):
        assert genre in collector.genre

    # 2. Дубликат книги не добавляется повторно в словарь books_genre
    def test_add_new_book_duplicate_book_not_added_again(self, collector):
        collector.add_new_book('Война и мир')
        collector.add_new_book('Война и мир')
        assert len(collector.books_genre) == 1

    # 3. Книге не устанавливается жанр, если его нет в списке доступных 
    @pytest.mark.parametrize('invalid_genre', ['Роман', 'Триллер'])
    def test_set_book_genre_invalid_genre_not_set(self, collector, invalid_genre):
        collector.add_new_book('Война и мир')
        collector.set_book_genre('Война и мир', invalid_genre)
        assert collector.books_genre['Война и мир'] == ''

    # 4. Получение жанра книги, существующей в словаре, по ее имени
    @pytest.mark.parametrize('genre', genres)
    def test_get_book_genre_existing_book_returns_genre(self, collector, genre):
        collector.add_new_book('Человек-амфибия')
        collector.set_book_genre('Человек-амфибия', genre)
        assert collector.get_book_genre('Человек-амфибия') == genre

    # 5. Метод возвращает только книгу с запрошенным жанром
    @pytest.mark.parametrize('genre, book_name', [
        ('Фантастика', 'Марсианские хроники'),
        ('Ужасы', 'Нечто'),
        ('Мультфильмы', 'Простоквашино'),
    ])
    def test_get_books_with_specific_genre_matching_genre_returns_book_list(self, collector, genre, book_name):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        result = collector.get_books_with_specific_genre(genre)
        assert result == [book_name]

    # 6. Метод get_books_genre возвращает текущий словарь books_genre
    def test_get_books_genre_returns_current_books_genre_dict(self, collector):
        collector.add_new_book('Веселые истории')
        collector.set_book_genre('Веселые истории', 'Комедии')
        assert collector.get_books_genre() == {'Веселые истории': 'Комедии'}

    # 7. Книга с жанром, имеющим возрастной рейтинг, не попадает в список книг для детей
    @pytest.mark.parametrize('age_rated_genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_age_rated_genre_book_excluded(self, collector, age_rated_genre):
        collector.add_new_book('Нечто')
        collector.set_book_genre('Нечто', age_rated_genre)
        assert collector.get_books_for_children() == []

    # 8. В избранное не добавляется книга, которой нет в словаре books_genre
    def test_add_book_in_favorites_book_not_in_books_genre_not_added(self, collector):
        collector.add_new_book('Марсианские хроники')
        collector.add_book_in_favorites('Война и мир')
        assert collector.favorites == []

    # 9. Успешное удаление книги из избранного
    def test_delete_book_from_favorites_existing_book_removed(self, collector):
        collector.add_new_book('Евгений Онегин')
        collector.add_book_in_favorites('Евгений Онегин')
        collector.delete_book_from_favorites('Евгений Онегин')
        assert collector.favorites == []

    # 10. Метод возвращает только список избранных книг
    def test_get_list_of_favorites_books_returns_only_favorites(self, collector):
        collector.add_new_book('Евгений Онегин')
        collector.add_new_book('Война и мир')
        collector.add_new_book('Гарри Поттер')
    
        collector.add_book_in_favorites('Евгений Онегин')
        collector.add_book_in_favorites('Война и мир')

        assert collector.get_list_of_favorites_books() == ['Евгений Онегин', 'Война и мир']
