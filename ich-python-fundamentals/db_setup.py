import mysql.connector

from config import dbconfig_edit, dbconfig_read, my_base


def get_connection(db_name=None, read_db=False):
    try:
        conn_params = dbconfig_read.copy() if read_db else dbconfig_edit.copy()
        if db_name:
            conn_params['database'] = db_name
        # print(f"Подключение к базе данных: "
        #       f"{conn_params.get('database', 'по умолчанию')}, "
        #       f"status: {'read' if read_db else 'edit'}")
        return mysql.connector.connect(**conn_params)

    except mysql.connector.Error as err:
        print(f"Ошибка подключения к базе данных: {err}")
        return None


def database_is_exists(db_name: str) -> bool:
    conn = get_connection(db_name)

    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = [db[0] for db in cursor.fetchall()]

            if db_name in databases:
                print(f"База данных '{db_name}' существует.")
                return True
            else:
                print(f"База данных '{db_name}' не существует.")
                return False

        except mysql.connector.Error as err:
            print(f"Ошибка при выполнении запроса: {err}")
            return False

        finally:
            cursor.close()
            conn.close()

    else:
        print("Не удалось подключиться к серверу MySQL.")
        return False


def create_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{my_base}`;")
        print(f"База данных {my_base} успешно создана или уже существует.")

        cursor.execute(f"USE `{my_base}`")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                login VARCHAR(20) NOT NULL UNIQUE
                CHECK (CHAR_LENGTH(login) >= 5),
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(30) NOT NULL UNIQUE,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                update_date DATETIME DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("Таблица users успешно создана.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query VARCHAR(200) NOT NULL,
                user_id INT NOT NULL,
                response JSON NOT NULL,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("Таблица queries успешно создана.")

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с MySQL закрыто.")
