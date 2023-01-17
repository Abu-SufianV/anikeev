import sqlite3 as sql


class DB:
    """
    Класс для взаимодействия с Базой Данных
    """

    def __init__(self, path: str):
        """
        Функция для подключения к базе данных

        :param path: путь до файла с базой данных SQLITE
        """
        self.path = path

    def product_in_db(self, rfid: str) -> list[bool | tuple]:
        """
        Функция поиска товара в базе данных

        Если товар найден, то возвращается True и кортеж с данными по этому товару,
        иначе возвращается False

        :param rfid: RFID-метка товара
        :return: [True, кортеж с данными по товару] | [False]
        """
        try:
            with sql.connect(self.path) as db:
                cursor = db.cursor()

                query = f"""SELECT * FROM products WHERE rfid = '{rfid}'"""
                product = cursor.execute(query).fetchone()

                if product:
                    return [True, product]
                return [False, ]
        except Exception as error:
            # Обработка ошибок при выполнении запроса
            print(query)
            print("Возникла ошибка при выполнении запроса на поиск товара:", error)

    def add_new_product(self, name: str, price: float, product_type: int, rfid: str) -> None:
        """
        Функция добавления нового товара в таблицу PRODUCTS

        :param name: Название товара
        :param price: Цена товара
        :param product_type: Тип товара
        :param rfid: RFID-метка товара
        """

        try:
            with sql.connect(self.path) as db:
                cursor = db.cursor()

                query = f"""INSERT INTO products VALUES (NULL,'{name}',{price},{product_type}, 1, '{rfid}')"""
                db.commit()

                cursor.execute(query)

                product = cursor.execute(f"""SELECT * FROM products WHERE rfid = '{rfid}'""").fetchone()
                print(f"Товар #{product[0]} {product[1]} добавлен успешно!")
        except Exception as error:
            # Обработка ошибок при выполнении запроса
            print(query)
            print("Возникла ошибка при выполнении запроса на создание товара:", error)

    def add_product(self, rfid: str) -> None:
        """
        Функция увеличения количества уже существующего товара

        :param rfid: RFID-метка товара
        """
        try:
            with sql.connect(self.path) as db:
                cursor = db.cursor()

                query = f"""UPDATE products SET amount = amount + 1 WHERE rfid = '{rfid}'"""
                db.commit()
                cursor.execute(query)
        except Exception as error:
            # Обработка ошибок при выполнении запроса
            print(query)
            print("\nERROR!\nВозникла ошибка при выполнении запроса на добавление товара:", error)

    def remove_unit_product(self, rfid: str) -> None:
        """
        Функция уменьшения количества/удаления уже существующего товара

        :param rfid: RFID-метка товара
        """
        try:
            with sql.connect(self.path) as db:
                cursor = db.cursor()

                query = f"""UPDATE products SET amount = amount - 1 WHERE rfid = '{rfid}'"""
                cursor.execute(query)
                db.commit()

                amount = cursor.execute(f"""SELECT amount FROM products WHERE rfid = '{rfid}'""").fetchone()[0]
                if amount == 0:
                    cursor.execute(f"""DELETE FROM products WHERE rfid = '{rfid}'""")
                    db.commit()

        except Exception as error:
            # Обработка ошибок при выполнении запроса
            print(query)
            print("Возникла ошибка при выполнении запроса на удаление товара:", error)

    def list_product_types(self) -> list[tuple]:
        """
        Функция вывода всех типов товаров
        """
        try:
            with sql.connect(self.path) as db:
                cursor = db.cursor()

                query = """SELECT * FROM PRODUCT_TYPE"""

                return cursor.execute(query).fetchall()

        except Exception as error:
            # Обработка ошибок при выполнении запроса
            print(query)
            print("Возникла ошибка при выполнении запроса:", error)
