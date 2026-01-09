"""
Главный модуль программы "Персональный бюджет".
Содержит точку входа и управление циклическим меню.
"""

import budget_data
import budget_actions
import budget_view
import budget_storage


def show_menu():
    """Выводит основное меню программы."""
    print("\n" + "=" * 60)
    print(" ПРОГРАММА 'ПЕРСОНАЛЬНЫЙ БЮДЖЕТ'")
    print("=" * 60)
    print("1. Отчет 1: Поступления за последние N дней")
    print("2. Отчет 2: Расходы по категории")
    print("3. Отчет 3: Расходы в определенное время")
    print("4. Просмотреть все транзакции")
    print("5. Добавить транзакцию")
    print("6. Редактировать транзакцию")
    print("7. Удалить транзакцию")
    print("0. Выход")
    print("-" * 60)
    print("Для выхода из любого меню введите 'назад'")


def main():
    """
    Основная функция управления программой.
    Запускает главный цикл с меню и обработкой выбора пользователя.
    """
    # Загрузка данных при старте
    database = budget_storage.load_transactions()
    if len(database) == 0:
        database = list(budget_data.transactions_db)
        print(f'Используются начальные данные: {len(database)} транзакций')
    else:
        print(f'Загружено {len(database)} транзакций из файла.')

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == '1':
            budget_actions.report_1_income_last_days(database)
        elif choice == '2':
            budget_actions.report_2_expenses_by_category(database)
        elif choice == '3':
            budget_actions.report_3_expenses_by_time(database)
        elif choice == '4':
            budget_view.display_transactions(database, "Все транзакции в базе")
        elif choice == '5':
            budget_actions.add_transaction(database)
        elif choice == '6':
            budget_actions.edit_transaction(database)
        elif choice == '7':
            budget_actions.delete_transaction(database)
        elif choice == '0':
            budget_storage.save_transactions(database)
            print("Выход из программы...")
            break
        else:
            print("Ошибка: Неверный пункт меню. Повторите ввод.")

        # Небольшая пауза для удобства чтения
        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()