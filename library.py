import json
import os


class Book:
    def __init__(self, id, title, author, year, status="в наличии"):
        """Инициализация книги как объекта класса"""
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """Преобразование книги из объекта класса в json формат"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    def __init__(self, data_file='library_data.json'):
        """Инициалиазция библиотеки"""
        self.data_file = data_file
        self.books = self.load_data()
        self.next_id = max((book.id for book in self.books), default=0) + 1

    def load_data(self):
        """Функция загрузки данных из файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        return []

    def save_data(self):
        """Функция сохранения данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """Функция добавления книги в библиотеку"""
        book = Book(id=self.next_id, title=title, author=author, year=year)
        self.books.append(book)
        self.next_id += 1
        self.save_data()
        print(f"Книга '{title}' добавлена.")

    def remove_book(self, book_id):
        """Функция удаления книги из библиотеки"""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_data()
                print(f"Книга '{book.title}' удалена.")
                return True
        print("Книга не найдена.")
        return False

    def search_books(self, query):
        """Функция поиска книги в библиотеке"""
        results = [book for book in self.books if query.lower() in book.title.lower() or
                   query.lower() in book.author.lower() or
                   query == str(book.year)]
        return results

    def display_books(self):
        """Функция вывода всех книг в библиотеке"""
        for book in self.books:
            print(f"{book.id}: '{book.title}' от {book.author}, {book.year} - {book.status}")

    def change_status(self, book_id, new_status):
        """Функция смена статуса книги"""
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_data()
                    print(f"Статус книги '{book.title}' изменен на '{new_status}'.")
                else:
                    print("Некорректный статус.")
                return
        print("Книга не найдена.")


def main():
    library = Library()

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == '2':
            try:
                book_id = int(input("Введите id книги для удаления: "))
                library.remove_book(book_id)
            except ValueError:
                print("Некорректный ввод.")

        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                print("Результаты поиска:")
                for book in results:
                    print(f"{book.id}: '{book.title}' от {book.author}, {book.year} - {book.status}")
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            try:
                book_id = int(input("Введите id книги: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                library.change_status(book_id, new_status)
            except ValueError:
                print("Некорректный ввод.")

        elif choice == '0':
            break
        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    main()
