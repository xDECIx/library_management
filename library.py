import json
from typing import List, Dict, Union


class Book:
    """
    Класс для представления книги.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги (в наличии/выдана).
    """

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализация объекта книги.

        Args:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги. По умолчанию "в наличии".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Преобразует объект книги в словарь.

        Returns:
            dict: Словарь с атрибутами книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, Union[int, str]]) -> 'Book':
        """
        Создает объект книги из словаря.

        Args:
            data (dict): Словарь с данными книги.

        Returns:
            Book: Объект книги.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    """
    Класс для управления библиотекой.

    Атрибуты:
        storage_file (str): Путь к файлу для хранения данных.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, storage_file: str):
        """
        Инициализация объекта библиотеки.

        Args:
            storage_file (str): Путь к файлу для хранения данных.
        """
        self.storage_file = storage_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """
        Загружает книги из файла.

        Если файл отсутствует, инициализирует пустую библиотеку.
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            self.books = []

    def save_books(self):
        """
        Сохраняет текущий список книг в файл.
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books],
                      file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.

        Returns:
            Book: Добавленная книга.
        """
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        return new_book

    def delete_book(self, book_id: int) -> bool:
        """
        Удаляет книгу по ID.

        Args:
            book_id (int): ID книги, которую нужно удалить.

        Returns:
            bool: True, если книга успешно удалена, иначе False.
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def search_books(self, keyword: str) -> List[Book]:
        """
        Выполняет поиск книг по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска (название, автор или год).

        Returns:
            List[Book]: Список книг, соответствующих ключевому слову.
        """
        return [
            book for book in self.books
            if keyword.lower() in book.title.lower()
            or keyword.lower() in book.author.lower()
            or str(book.year) == keyword
        ]

    def update_status(self, book_id: int, new_status: str) -> bool:
        """
        Изменяет статус книги.

        Args:
            book_id (int): ID книги.
            new_status (str): Новый статус книги ("в наличии" или "выдана").

        Returns:
            bool: True, если статус успешно обновлен, иначе False.
        """
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return True
        return False

    def get_all_books(self) -> List[Book]:
        """
        Возвращает список всех книг в библиотеке.

        Returns:
            List[Book]: Список всех книг.
        """
        return self.books
