"""
Модуль для безопасного ввода данных бюджета.
Содержит функции для проверки типов вводимых значений.
"""

from budget_data import is_valid_time, parse_time


def get_integer(prompt, min_value=None, max_value=None):
    """
    Запрашивает у пользователя целое число с валидацией.

    Args:
        prompt (str): Текст приглашения для ввода
        min_value (int, optional): Минимальное допустимое значение
        max_value (int, optional): Максимальное допустимое значение

    Returns:
        int: Введенное целое число или None если ввод отменен
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'назад':
            return None

        try:
            value = int(user_input)

            if min_value is not None and value < min_value:
                print(f"Ошибка: значение должно быть не меньше {min_value}")
                continue

            if max_value is not None and value > max_value:
                print(f"Ошибка: значение должно быть не больше {max_value}")
                continue

            return value
        except ValueError:
            print("Ошибка: введите целое число (или 'назад' для отмены)")


def get_float(prompt):
    """
    Запрашивает у пользователя вещественное число с валидацией.

    Args:
        prompt (str): Текст приглашения для ввода

    Returns:
        float: Введенное вещественное число или None если ввод отменен
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'назад':
            return None

        try:
            value = float(user_input)

            if value <= 0:
                print("Ошибка: сумма должна быть положительной")
                continue

            return value
        except ValueError:
            print("Ошибка: введите число (можно с точкой) "
                  "или 'назад' для отмены.")


def get_string(prompt):
    """
    Запрашивает непустую строку с валидацией.

    Args:
        prompt (str): Текст приглашения для ввода

    Returns:
        str: Введенная строка или None если ввод отменен
    """
    while True:
        value = input(prompt).strip()
        
        if value.lower() == 'назад':
            return None

        if len(value) > 0:
            return value
        print("Ошибка: введите непустую строку (или 'назад' для отмены)")


def get_time(prompt):
    """
    Получает время от пользователя в формате HH:MM с валидацией.

    Args:
        prompt (str): Приглашение для ввода

    Returns:
        tuple: Кортеж (час, минута) или None если ввод отменен
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'назад':
            return None

        if not is_valid_time(user_input):
            print("Ошибка: время должно быть в формате"
                  " HH:MM (например, 14:30)")
            continue

        hour, minute = parse_time(user_input)
        return hour, minute