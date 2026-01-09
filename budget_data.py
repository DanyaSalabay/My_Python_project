"""
Модуль с базой данных транзакций и вспомогательными функциями.
Содержит исходные данные и функции для работы с датами и временем.
"""

# База данных транзакций (минимум 25 записей)
transactions_db = list([
    ("2026-01-15", "09:30", "приход", "зарплата", 50000, "Компания А"),
    ("2026-01-15", "10:15", "расход", "питание", 1500, "Супермаркет Б"),
    ("2026-01-15", "18:45", "расход", "развлечения", 3000, "Кинотеатр В"),
    ("2026-01-16", "08:20", "расход", "транспорт", 500, "Такси Г"),
    ("2026-01-16", "12:30", "расход", "питание", 1200, "Кафе Д"),
    ("2026-01-16", "19:00", "расход", "развлечения", 2500, "Ресторан Е"),
    ("2026-01-17", "10:00", "приход", "аванс", 20000, "Компания А"),
    ("2026-01-17", "13:45", "расход", "транспорт", 400, "Метро"),
    ("2026-01-17", "20:30", "расход", "развлечения", 1800, "Бар Ж"),
    ("2026-01-18", "09:15", "приход", "подарок", 10000, "Друг З"),
    ("2026-01-18", "11:30", "расход", "питание", 900, "Столовая И"),
    ("2026-01-18", "18:20", "расход", "транспорт", 600, "Автобус"),
    ("2026-01-19", "14:00", "расход", "развлечения", 3500, "Концерт К"),
    ("2026-01-19", "19:45", "расход", "питание", 2000, "Ресторан Л"),
    ("2026-01-20", "10:30", "приход", "зарплата", 45000, "Компания М"),
    ("2026-01-20", "12:15", "расход", "питание", 800, "Кафе Н"),
    ("2026-01-20", "20:00", "расход", "развлечения", 2800, "Театр О"),
    ("2026-01-21", "08:45", "расход", "транспорт", 550, "Такси П"),
    ("2026-01-21", "13:30", "расход", "питание", 1100, "Столовая Р"),
    ("2026-01-21", "21:15", "расход", "развлечения", 1500, "Кино С"),
    ("2026-01-22", "11:00", "приход", "подарок", 5000, "Коллега Т"),
    ("2026-01-22", "18:30", "расход", "транспорт", 450, "Метро"),
    ("2026-01-22", "20:45", "расход", "развлечения", 3200, "Ресторан У"),
    ("2026-01-23", "09:45", "расход", "питание", 700, "Булочная Ф"),
    ("2026-01-23", "19:30", "расход", "развлечения", 2200, "Бар Х"),
    ("2026-01-24", "10:20", "приход", "аванс", 15000, "Компания А"),
    ("2026-01-24", "12:45", "расход", "питание", 1300, "Кафе Ц"),
    ("2026-01-24", "21:00", "расход", "развлечения", 1900, "Клуб Ч")
])

# Список возможных категорий
categories = list(["питание", "транспорт", "развлечения",
                   "зарплата", "аванс", "подарок"])

def is_valid_date(date_string):
    """
    Проверяет, является ли строка корректной датой в формате YYYY-MM-DD.

    Args:
        date_string (str): Строка с датой для проверки

    Returns:
        bool: True если дата корректна, иначе False
    """
    try:
        if len(date_string) != 10:
            return False
        if date_string[4] != '-' or date_string[7] != '-':
            return False

        year_part = date_string[0:4]
        month_part = date_string[5:7]
        day_part = date_string[8:10]

        if (not year_part.isdigit() or not month_part.isdigit() or
                not day_part.isdigit()):
            return False

        month_number = int(month_part)
        day_number = int(day_part)

        if month_number < 1 or month_number > 12:
            return False
        if month_number in [1, 3, 5, 7, 8, 10, 12]:
            if day_number < 1 or day_number > 31:
                return False
        elif month_number in [4, 6, 9, 11]:
            if day_number < 1 or day_number > 30:
                return False
        else:
            is_leap_year = (year_part % 400 == 0) or (year_part % 4 == 0 and
                                                      year_part % 100 != 0)
            max_day = 29 if is_leap_year else 28
            if day_number < 1 or day_number > max_day:
                return False

        return True
    except Exception:
        return False


def is_valid_time(time_string):
    """
    Проверяет, является ли строка корректным временем в формате HH:MM.

    Args:
        time_string (str): Строка со временем для проверки

    Returns:
        bool: True если время корректно, иначе False
    """
    try:
        if len(time_string) != 5:
            return False
        if time_string[2] != ':':
            return False

        hour_part = time_string[0:2]
        minute_part = time_string[3:5]

        if not hour_part.isdigit() or not minute_part.isdigit():
            return False

        hour_number = int(hour_part)
        minute_number = int(minute_part)

        if hour_number < 0 or hour_number > 23:
            return False
        if minute_number < 0 or minute_number > 59:
            return False

        return True
    except Exception:
        return False


def parse_date(date_string):
    """
    Парсит строку даты в кортеж чисел для сравнения.

    Args:
        date_string (str): Дата в формате YYYY-MM-DD

    Returns:
        tuple: Кортеж (год, месяц, день) в виде целых чисел
    """
    year_number = int(date_string[0:4])
    month_number = int(date_string[5:7])
    day_number = int(date_string[8:10])
    return (year_number, month_number, day_number)


def parse_time(time_string):
    """
    Парсит строку времени в кортеж чисел для сравнения.

    Args:
        time_string (str): Время в формате HH:MM

    Returns:
        tuple: Кортеж (час, минута) в виде целых чисел
    """
    hour_number = int(time_string[0:2])
    minute_number = int(time_string[3:5])
    return (hour_number, minute_number)


def is_time_in_range(time_string, start_hour, start_minute,
                     end_hour, end_minute):
    """
    Проверяет, находится ли время в указанном диапазоне.

    Args:
        time_string (str): Время в формате HH:MM
        start_hour (int): Начальный час диапазона
        start_minute (int): Начальная минута диапазона
        end_hour (int): Конечный час диапазона
        end_minute (int): Конечная минута диапазона

    Returns:
        bool: True если время в диапазоне, иначе False
    """
    hour, minute = parse_time(time_string)
    start_time_in_minutes = start_hour * 60 + start_minute
    end_time_in_minutes = end_hour * 60 + end_minute
    current_time_in_minutes = hour * 60 + minute
    return (start_time_in_minutes <= current_time_in_minutes
            <= end_time_in_minutes)