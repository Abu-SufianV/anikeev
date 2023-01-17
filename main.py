import db

db = db.DB('db.sqlite')


def add_product(rfid: str) -> None:
    """
    Интерфейс добавления товара в базу данных через терминал

    :param rfid: RFID-метка товара
    """
    print()
    name = input('Название: ')
    price = int(input('Цена: '))

    print("\nСуществующие типы товаров:")
    for row in db.list_product_types():
        print(f"\t{row[0]}. {row[1]}")
    pr_type = int(input('Номер типа товара: '))
    print()
    db.add_new_product(name, price, pr_type, rfid)


# db.add_new_product('Tommy Jeans', 15000, 1,  'Rx[09954]')
# db.add_new_product('H&M', 2400, 2,  'Rx[15710]')
# db.add_new_product('Levi`s', 15000, 1,  'Rx[51541]')
# db.add_new_product('Gucci', 35000, 4,  'Rx[97867]')

# db.remove_unit_product('Rx[51541]')

# print(db.product_in_db('Rx[15710]'))
if __name__ == '__main__':
    print('Приложение запущено...')
    while True:
        event = int(input('\nEvent: '))

        if event == 1:
            # Симуляция турникета на завоз товаров на склад
            print(f"ЗАВОЗ товара на склад")
            # Симуляция считывания RFID-метки
            pr_rfid = input('RFID-метка: ')
            product = db.product_in_db(pr_rfid)

            if product[0]:
                print()
                db.add_product(pr_rfid)
                print(f"Товар {pr_rfid} завезён на склад")
                print(f"Название: {product[1][1]}")
                print(f"Цена: {product[1][2]}")
                print(f"Кол-во: {product[1][4]} шт. -> {product[1][4]+1} шт.")
                print()
                del product

            else:
                print()
                print(f"Товар {pr_rfid} не найден в базе ")
                add_pr = input("Добавить товар? (Да/Нет): ").lower().strip()
                if add_pr in ["да", "д", "yes", "y"]:
                    add_product(pr_rfid)
        elif event == 2:
            # Симуляция турникета на вывоз товаров из склада
            print(f"ВЫВОЗ товара со склада")
            # Симуляция считывания RFID-метки
            pr_rfid = input('RFID-метка: ')
            product = db.product_in_db(pr_rfid)

            if product[0]:
                print()
                db.remove_unit_product(pr_rfid)
                print(f"Товар {pr_rfid} вывезен со склада")
                if product[1][4] > 1:
                    print(f"Название: {product[1][1]}")
                    print(f"Цена: {product[1][2]}")
                    print(f"Кол-во: {product[1][4]} шт. -> {product[1][4]+1} шт.")
                else:
                    print("На складе больше нет единиц данного товара")
                    print("Запись о нём удалена из БД")
            else:
                print(f"\nТовар {pr_rfid} не найден в базе ")
        elif event == 0:
            # Симуляция отключения системы
            print(' - - - - - - - - - - -')
            print('Приложение остановлено')
            break
        else:
            # Симуляция некорректного считывания RFID-метки
            print("Команда не распознана\nПопробуйте повторно")