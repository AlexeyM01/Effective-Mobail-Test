import unittest
import os
import json
from library import Library, Book
import io
import sys


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Настройка тестов: создание временного файла для тестирования."""
        self.library = Library(data_file='test_library_data.json')
        self.library.books = []  # Очистим список книг
        self.library.next_id = 1  # Восстанавливаем ID

    def tearDown(self):
        """Очистка после тестов: удаление временного файла."""
        if os.path.exists('test_library_data.json'):
            os.remove('test_library_data.json')

    def test_add_book(self):
        """Тест на добавление книги."""
        self.library.add_book("Тестовая книга", "Тестовый автор", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Тестовая книга")

    def test_remove_book(self):
        """Тест на удаление книги."""
        self.library.add_book("Книга для удаления", "Автор", 2023)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        """Тест на попытку удалить несуществующую книгу."""
        # Перенаправляем вывод в строку
        output = io.StringIO()
        sys.stdout = output

        self.library.remove_book(999)  # Используем несуществующий ID
        sys.stdout = sys.__stdout__  # Восстанавливаем стандартный вывод

        self.assertIn("Книга не найдена.", output.getvalue())

    def test_search_books(self):
        """Тест на поиск книг."""
        self.library.add_book("Тестовая книга", "Тестовый автор", 2023)
        self.library.add_book("Другая книга", "Другой автор", 2022)

        results = self.library.search_books("Тестовая")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Тестовая книга")

        results = self.library.search_books("2022")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Другая книга")

    def test_display_books(self):
        """Тест на отображение книг (проверяет, что книга добавлена)."""
        self.library.add_book("Книга для отображения", "Автор", 2023)
        output = io.StringIO()
        sys.stdout = output
        self.library.display_books()
        sys.stdout = sys.__stdout__
        self.assertIn("Книга для отображения", output.getvalue())

    def test_change_status(self):
        """Тест на изменение статуса книги."""
        self.library.add_book("Книга для статуса", "Автор", 2023)
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_change_status_invalid(self):
        """Тест на изменение статуса с некорректным значением."""
        self.library.add_book("Книга для проверки статуса", "Автор", 2023)
        book_id = self.library.books[0].id

        # Перенаправляем вывод в строку
        output = io.StringIO()
        sys.stdout = output

        self.library.change_status(book_id, "некорректный статус")

        sys.stdout = sys.__stdout__  # Восстанавливаем стандартный вывод
        self.assertIn("Некорректный статус.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
