from config import my_base, file_dir
import re
import json

from db_operations import (
    add_log_search_query,
    add_user_to_database,
    all_query_one_user,
    all_query_users,
    all_films_from_query,
    change_user_information,
    fetch_table_rows,
    fetch_user_email,
    fetch_user_info,
    find_all_films_and_film_id,
    find_films_from_actor,
    find_film_year_and_genre,
    find_current_user_id,
    user_exists_in_database,
)

from db_setup import (
    create_database,
    database_is_exists,
)

from search_enginee import (
    films_rating,
    find_documents,
    parse_stop_words,
    rating_query_users,
)


def main():
    if not database_is_exists(my_base):
        create_database()

    input_login = input("\nДля входа в систему введите ваш логин: ")

    if user_exists_in_database(input_login):
        login_data = fetch_user_info(input_login)
        print(f"\nДобро пожаловать {login_data['first_name']} "
              f"{login_data['last_name']}!")
    else:
        while True:
            first_name = input("Необходимо выполнить регистрацию. "
                               "Введите, пожалуйста, ваше имя: ").title()
            if not first_name:
                print("Данное поле не может быть пустым.")
                continue
            break

        while True:
            last_name = input("Введите вашу фамилию: ").title()
            if not last_name:
                print("Данное поле не может быть пустым.")
                continue
            break

        while True:
            email = input("Последним шагом необходимо ввести email: ")

            if not email:
                print("Ошибка: Email не может быть пустым.")
                continue

            email_pattern = r'^[a-zA-Z0-9_.+-]+' \
                            r'@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if not re.match(email_pattern, email):
                print("Ошибка: некорректный email.")
                continue

            if fetch_user_email(email):
                print("Данный email уже зарегистрирован. "
                      "Пожалуйста, введите другой")
                choice = input(
                    "Хотите ввести другой email? (да/нет): ").lower()
                if choice != "да":
                    print("К сожалению, вы не выполнили регистрацию")
                    exit()
            else:
                break

        add_user_to_database(input_login, first_name, last_name, email)

        print(f"\nРегистрация прошла успешно! Добро пожаловать "
              f"{first_name} {last_name}!")

    while True:
        print("\nГлавное меню:\n"
              "\n1 - Найти фильм"
              "\n2 - Получить статистику"
              "\n3 - Изменить свои данные"
              "\n0 - Выход из программы.\n")
        action = input("Выберите действие: ")
        if action == "1":
            while True:
                print("\nВарианты для поиска:\n"
                      "\n1 - Найти фильмы по году и жанру"
                      "\n2 - Поиск фильма по ключевым словам"
                      "\n3 - Поиск фильма по фамилии актера"
                      "\n4 - Поиск фильмов по популярности"
                      "\n0 - Назад\n")
                choice = input("Выберите вариант поиска: ")

                if choice == "0":
                    print("Выход из режима поиска.")
                    break

                if choice == "1":
                    while True:
                        input_year = input("Введите год выпуска фильма "
                                           "(если известен): ")

                        if input_year == "":
                            year = None
                            break

                        try:
                            year = int(input_year)
                            break
                        except ValueError:
                            print("Ошибка: Введите корректный год "
                                  "(целое число). Попробуйте снова.")

                    input_genre = input("Введите жанр фильма "
                                        "(если знаете): ").lower()
                    genre = input_genre if input_genre else None

                    films = find_film_year_and_genre(year, genre)

                    if not films:
                        print("По вашему запросу ничего не найдено.")
                    else:
                        print("\nНайденные фильмы: ")

                        for _, film_title in films:
                            print(film_title)

                    found_film_ids = json.dumps(
                        [film_id for film_id, _ in films])

                    user_id = find_current_user_id(input_login)

                    user_query = f"{year}, {genre}"

                    add_log_search_query(user_query, user_id, found_film_ids)

                    break

                if choice == "2":
                    user_query = input("Введите описание фильма: ").lower()

                    stop_words = parse_stop_words(file_dir)
                    documents = fetch_table_rows()

                    films = find_documents(documents, stop_words, user_query)

                    if not films:
                        print("Фильмы не найдены.")
                        films_sorted = []
                    else:
                        films_sorted = sorted(
                            films, key=lambda x: x[1], reverse=True)

                    all_film_titles = find_all_films_and_film_id()

                    print("\nНайденные фильмы:")

                    for film_id, count in films_sorted:
                        film_title = all_film_titles[film_id]
                        print(f"Название фильма: {film_title}, "
                              f"Количество совпадений: {count}")

                    found_film_ids = json.dumps(
                        [film[0] for film in films_sorted])

                    user_id = find_current_user_id(input_login)

                    add_log_search_query(user_query, user_id, found_film_ids)

                if choice == "3":
                    input_actor = input("Введите фамилию актёра: ").upper()
                    films_from_actor = find_films_from_actor(input_actor)

                    if films_from_actor:
                        for _, film in films_from_actor:
                            print(film)
                    else:
                        print("Фильмы с данным актёром не найдены.")

                    found_film_ids = json.dumps(
                        [film_id for film_id, _ in films_from_actor])

                    user_id = find_current_user_id(input_login)

                    add_log_search_query(input_actor, user_id, found_film_ids)

                if choice == "4":
                    query_film_ids = all_films_from_query()
                    film_id_and_count = films_rating(query_film_ids)
                    all_film_titles = find_all_films_and_film_id()

                    for film_id, count in film_id_and_count:
                        film_title = all_film_titles[film_id]
                        print(f"Название фильма: {film_title}, "
                              f"Количество совпадений: {count}")

        if action == "2":
            while True:
                print("\nВарианты для поиска:\n"
                      "\n1 - Ваши запросы"
                      "\n2 - Все запросы пользователей"
                      "\n3 - Вывести статистику по самым популярным запросам"
                      "\n0 - Назад\n")
                choice = input("Выберите вариант поиска: ")

                if choice == "0":
                    print("Выход из режима поиска.")
                    break

                if choice == "1":
                    statistics_user = all_query_one_user(input_login)

                    print("\nСписок ваших запросов:")
                    print("\n".join(statistics_user))

                if choice == "2":
                    statistics_all_users = all_query_users()

                    print("\nСписок запросов всех пользователей:")
                    print("\n".join(statistics_all_users))

                if choice == "3":

                    queries = all_query_users()
                    rating_query_users(queries)

        elif action == "3":
            while True:
                print("\nВарианты для изменения:\n"
                      "\n1 - Изменить login"
                      "\n2 - Изменить first_name"
                      "\n3 - Изменить last_name"
                      "\n4 - Изменить email"
                      "\n0 - Назад\n")
                field_action = input("Выберите изменение: ")

                if field_action == "0":
                    print("Выход из режима обновления данных.")
                    break

                field_map = {
                    "1": "login",
                    "2": "first_name",
                    "3": "last_name",
                    "4": "email",
                }

                if field_action in field_map:
                    field_name = field_map[field_action]

                while True:
                    new_value = input(f"Введите новое значение для "
                                      f"{field_name}: ")

                    if not new_value:
                        print(f"Ошибка: {field_name} не может быть пустым.")
                        continue

                    if field_name == "login":
                        if user_exists_in_database(new_value):
                            print("Данный логин уже существует, "
                                  "попробуйте другой.")
                            continue

                        if len(new_value) < 5:
                            print("Логин должен содержать "
                                  "не менее 5 символов.")
                            continue

                    if field_name == "email":
                        email_pattern = r'^[a-zA-Z0-9_.+-]+' \
                                        r'@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

                        if not re.match(email_pattern, new_value):
                            print("Ошибка: некорректный email.")
                            continue

                        if fetch_user_email(new_value):
                            print("Данный email уже зарегистрирован. "
                                  "Пожалуйста, введите другой")
                            continue

                    change = change_user_information(my_base, input_login,
                                                     field_name, new_value)

                    if change:
                        if field_name == "login":
                            input_login = new_value
                        break

        elif action == "0":
            print("Выход из программы.")
            break


if __name__ == "__main__":
    main()
