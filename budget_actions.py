"""
Модуль бизнес-логики бюджета.
Содержит функции для CRUD операций и подготовки данных для отчетов.
"""

import budget_input
import budget_view
import budget_sorter
import budget_storage
from budget_data import categories, is_valid_date, is_valid_time


def show_section_header(title):
    """
    Отображает заголовок раздела программы.

    Args:
        title (str): Текст заголовка для отображения
    """
    print(f"\n{'=' * 60}")
    print(title)
    print('=' * 60)
    print("(введите 'назад' на любом этапе для отмены)\n")


def add_transaction(data_list):
    """
    Добавляет новую транзакцию в базу данных.

    Args:
        data_list (list): Текущая база данных транзакций
    """
    show_section_header("ДОБАВЛЕНИЕ НОВОЙ ТРАНЗАКЦИИ")
    
    # Дата
    while True:
        date_input = budget_input.get_string("Дата (ГГГГ-ММ-ДД): ")
        if date_input is None:
            print("Отмена добавления транзакции.")
            return
        if not is_valid_date(date_input):
            print("Ошибка: неверный формат даты. Пример: 2026-01-15")
            continue
        break
    
    # Время
    while True:
        time_input = budget_input.get_string("Время (ЧЧ:ММ): ")
        if time_input is None:
            print("Отмена добавления транзакции.")
            return
        if not is_valid_time(time_input):
            print("Ошибка: неверный формат времени. Пример: 14:30")
            continue
        break
    
    # Направление
    while True:
        direction_input = (budget_input.get_string
                           ("Направление (приход/расход): "))
        if direction_input is None:
            print("Отмена добавления транзакции.")
            return
        if direction_input not in ['приход', 'расход']:
            print("Ошибка: должно быть 'приход' или 'расход'")
            continue
        break
    
    # Категория
    print("\nДоступные категории:", ', '.join(categories))
    while True:
        category_input = budget_input.get_string("Категория: ")
        if category_input is None:
            print("Отмена добавления транзакции.")
            return
        if category_input not in categories:
            print(f"Ошибка: категория должна быть одной из: "
                  f"{', '.join(categories)}")
            continue
        break
    
    # Сумма
    while True:
        amount_input = budget_input.get_float("Сумма (руб.): ")
        if amount_input is None:
            print("Отмена добавления транзакции.")
            return
        break
    
    # Контрагент
    while True:
        contractor_input = budget_input.get_string("Контрагент: ")
        if contractor_input is None:
            print("Отмена добавления транзакции.")
            return
        break

    new_trans = (date_input, time_input, direction_input,
                      category_input, amount_input, contractor_input)
    data_list.append(new_trans)
    print(f"\n Транзакция успешно добавлена! Всего транзакций:"
          f" {len(data_list)}")
    budget_storage.save_transactions(data_list)


def delete_transaction(data_list):
    """
    Удаляет транзакцию по номеру в списке.

    Args:
        data_list (list): Текущая база данных транзакций
    """
    show_section_header("УДАЛЕНИЕ ТРАНЗАКЦИИ")
    
    if not data_list:
        print("Нет транзакций для удаления.")
        return
    
    budget_view.display_transactions(data_list,
                                     "Выберите транзакцию для удаления")
    
    index_num = budget_input.get_integer(
        "Введите номер транзакции для удаления: ", 1, len(data_list))
    if index_num is None:
        print("Отмена удаления.")
        return
    
    removed_trans = data_list.pop(index_num - 1)
    print(f"\n Транзакция удалена")
    budget_view.display_transaction(removed_trans)
    print(f"Осталось транзакций: {len(data_list)}")
    budget_storage.save_transactions(data_list)


def edit_transaction(data_list):
    """
    Редактирует транзакцию по номеру.

    Args:
        data_list (list): Текущая база данных транзакций
    """
    show_section_header("РЕДАКТИРОВАНИЕ ТРАНЗАКЦИИ")
    
    if not data_list:
        print("Нет транзакций для редактирования.")
        return
    
    budget_view.display_transactions(data_list,
                                     "Выберите транзакцию для редактирования")
    
    index_num = budget_input.get_integer(
        "Введите номер транзакции: ", 1, len(data_list))
    if index_num is None:
        print("Отмена редактирования.")
        return
    
    trans_data = list(data_list[index_num - 1])
    print("\nТекущие данные:")
    budget_view.display_transaction(trans_data)
    print("\nВведите новые значения (оставьте пустым для сохранения старого):")
    
    # Обновление каждого поля
    new_values = list()
    field_names = ["Дата", "Время", "Направление",
                   "Категория", "Сумма", "Контрагент"]
    
    for field_idx, (field_name, current_value) in\
            enumerate(zip(field_names, trans_data)):
        if field_idx == 3:  # Категория
            print(f"\nДоступные категории: {', '.join(categories)}")
        
        while True:
            user_input = input(f"{field_name} [{current_value}]: ").strip()
            
            if user_input.lower() == 'назад':
                print("Отмена редактирования.")
                return
            
            if not user_input:
                new_values.append(current_value)
                break
            
            # Валидация для каждого поля
            if field_idx == 0 and not is_valid_date(user_input):
                print("Ошибка: неверный формат даты (ГГГГ-ММ-ДД)")
                continue
            elif field_idx == 1 and not is_valid_time(user_input):
                print("Ошибка: неверный формат времени (ЧЧ:ММ)")
                continue
            elif field_idx == 2 and user_input not in ['приход', 'расход']:
                print("Ошибка: должно быть 'приход' или 'расход'")
                continue
            elif field_idx == 3 and user_input not in categories:
                print(f"Ошибка: категория должна быть одной из:"
                      f" {', '.join(categories)}")
                continue
            elif field_idx == 4:
                try:
                    amount_value = float(user_input)
                    if amount_value <= 0:
                        print("Ошибка: сумма должна быть положительной")
                        continue
                    new_values.append(amount_value)
                    break
                except ValueError:
                    print("Ошибка: введите число")
                    continue
            elif field_idx == 5 and not user_input.strip():
                print("Ошибка: контрагент не может быть пустым")
                continue
            
            new_values.append(user_input)
            break
    
    data_list[index_num - 1] = tuple(new_values)
    print("\n Транзакция успешно обновлена!")
    budget_storage.save_transactions(data_list)


def filter_transactions_by_days(transactions, days):
    """
    Фильтрует транзакции за последние N дней.

    Args:
        transactions (list): Список транзакций для фильтрации
        days (int): Количество дней для фильтрации

    Returns:
        list: Отфильтрованный список транзакций
    """
    if days <= 0:
        return list()

    from budget_data import parse_date
    while True:
        today_str = input('Введите сегодняшнюю дату (ГГГГ-ММ-ДД): ')
        if not is_valid_date(today_str):
            print('Некорректный формат даты!')
            continue
        break
    today_year, today_month, today_day = parse_date(today_str)

    filtered = list()
    for trans in transactions:
        if trans[2] != "приход":
            continue

        trans_date_str = trans[0]
        trans_year, trans_month, trans_day = parse_date(trans_date_str)

        # Упрощенная проверка для демонстрации
        if today_year == trans_year and today_month == trans_month:
            if today_day - trans_day <= days:
                filtered.append(trans)

    return filtered


def filter_transactions_by_category(transactions, category_name):
    """
    Фильтрует транзакции по категории.

    Args:
        transactions (list): Список транзакций для фильтрации
        category_name (str): Категория для фильтрации

    Returns:
        list: Отфильтрованный список транзакций
    """
    filtered = list()
    for trans in transactions:
        if trans[2] == "расход" and trans[3] == category_name:
            filtered.append(trans)
    return filtered


def filter_transactions_by_time_range\
                (transactions, start_hour, start_minute, end_hour, end_minute):
    """
    Фильтрует транзакции по временному промежутку.

    Args:
        transactions (list): Список транзакций для фильтрации
        start_hour (int): Начальный час диапазона
        start_minute (int): Начальная минута диапазона
        end_hour (int): Конечный час диапазона
        end_minute (int): Конечная минута диапазона

    Returns:
        list: Отфильтрованный список транзакций
    """
    filtered = list()
    for trans in transactions:
        if trans[2] != "расход":
            continue

        time_str = trans[1]
        from budget_data import is_time_in_range
        if (is_time_in_range
            (time_str, start_hour, start_minute, end_hour, end_minute)):
            filtered.append(trans)
    return filtered


def report_1_income_last_days(data_list):
    """
    Отчет 1: Поступления за последние N дней.
    Сортировка: дата (убыв) + сумма (убыв).
    """
    show_section_header("ОТЧЕТ 1: ПОСТУПЛЕНИЯ ЗА ПОСЛЕДНИЕ N ДНЕЙ")
    
    days = budget_input.get_integer("Введите количество дней (N): ", 1)
    if days is None:
        print("Отмена отчета.")
        return
    
    filtered = filter_transactions_by_days(data_list, days)
    sorted_data = (budget_sorter.heap_sort
                   (filtered, budget_sorter.compare_income_by_date_desc_amount_desc))
    
    if sorted_data:
        (budget_view.display_transactions
         (sorted_data, f"Поступления за последние {days} дней"))
    else:
        print(f"\nНет поступлений за последние {days} дней.")


def report_2_expenses_by_category(data_list):
    """
    Отчет 2: Расходы по категории.
    Сортировка: дата (убыв) + контрагент (возр) + сумма (убыв).
    """
    show_section_header("ОТЧЕТ 2: РАСХОДЫ ПО КАТЕГОРИИ")
    
    print("Доступные категории расходов:")
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")
    
    while True:
        user_input = input("\nВведите номер категории или её название: ")
        if user_input.lower() == 'назад':
            print("Отмена отчета.")
            return

        try:
            choice_num = int(user_input)
            if 1 <= choice_num <= len(categories):
                selected_category = categories[choice_num - 1]
                break
            else:
                print(f"Ошибка: номер должен быть от 1 до {len(categories)}")
                continue
        except ValueError:
            if user_input in categories:
                selected_category = user_input
                break
            else:
                print(f"Ошибка: категория '{user_input}' не найдена")
                print(f"Доступные категории: {', '.join(categories)}")
                continue
    
    filtered = filter_transactions_by_category(data_list, selected_category)
    sorted_data = budget_sorter.heap_sort(filtered,
                                          budget_sorter.compare_expenses_by_date_desc_contractor_asc_amount_desc)
    
    if sorted_data:
        (budget_view.display_transactions
         (sorted_data, f"Расходы по категории '{selected_category}'"))
    else:
        print(f"\nНет расходов по категории '{selected_category}'.")


def report_3_expenses_by_time(data_list):
    """
    Отчет 3: Расходы в определенное время.
    Сортировка: сумма (убыв) + контрагент (возр) + дата (убыв).
    """
    show_section_header("ОТЧЕТ 3: РАСХОДЫ В ОПРЕДЕЛЕННОЕ ВРЕМЯ")
    
    print("Пример: для промежутка с 18:00 до 21:00")
    print("Введите время начала: 18:00")
    print("Введите время окончания: 21:00\n")

    # Время начала
    while True:
        start_time = budget_input.get_time("Введите время начала (HH:MM): ")
        if start_time is None:
            print("Отмена отчета.")
            return
        break

    # Время окончания
    while True:
        end_time = budget_input.get_time("Введите время окончания (HH:MM): ")
        if end_time is None:
            print("Отмена отчета.")
            return
        break

    start_hour, start_minute = start_time
    end_hour, end_minute = end_time

    start_total = start_hour * 60 + start_minute
    end_total = end_hour * 60 + end_minute

    if start_total >= end_total:
        print("Ошибка: время начала должно быть меньше времени окончания")
        return

    filtered = (filter_transactions_by_time_range
                (data_list, start_hour, start_minute, end_hour, end_minute))
    sorted_data = budget_sorter.heap_sort(filtered,
                                          budget_sorter.compare_expenses_by_time_range_amount_desc_contractor_asc)
    
    if sorted_data:
        title = (f"Расходы с {start_hour:02d}:{start_minute:02d}"
                 f" до {end_hour:02d}:{end_minute:02d}")
        budget_view.display_transactions(sorted_data, title)
    else:
        print(f"\nНет расходов с {start_hour:02d}:{start_minute:02d}"
              f" до {end_hour:02d}:{end_minute:02d}")