from library import Library


def main():
    library = Library("storage.json")

    while True:
        print("\n=== Управление библиотекой ===")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            book = library.add_book(title, author, year)
            print(f"Книга добавлена: {book.to_dict()}")

        elif choice == "2":
            book_id = int(input("Введите ID книги: "))
            if library.delete_book(book_id):
                print("Книга удалена.")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == "3":
            keyword = input(
                "Введите название, автора или год издания для поиска: ")
            results = library.search_books(keyword)
            if results:
                for book in results:
                    print(book.to_dict())
            else:
                print("Книги не найдены.")

        elif choice == "4":
            books = library.get_all_books()
            if books:
                for book in books:
                    print(book.to_dict())
            else:
                print("Библиотека пуста.")

        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            if library.update_status(book_id, new_status):
                print("Статус книги обновлен.")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
