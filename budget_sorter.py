"""
Модуль сортировки бюджета.
Реализует алгоритм пирамидальной сортировки и логику сравнения
для различных типов отчетов бюджета.
"""

def copy_list(original):
    """
    Создает глубокую копию списка транзакций.

    Args:
        original (list): Исходный список транзакций для копирования

    Returns:
        list: Новая копия списка транзакций
    """
    copied = list()
    for item in original:
        copied.append(item)
    return copied


def heapify(array_data, heap_size, root_index, compare_func):
    """
    Вспомогательная функция для построения кучи (пирамиды).

    Args:
        array_data (list): Массив для сортировки
        heap_size (int): Размер кучи
        root_index (int): Индекс корня поддерева
        compare_func (function): Функция сравнения элементов
                                для определения порядка
    """
    largest_index = root_index
    left_index = 2 * root_index + 1
    right_index = 2 * root_index + 2

    if left_index < heap_size and compare_func(array_data[left_index],
                                               array_data[largest_index]):
        largest_index = left_index

    if right_index < heap_size and compare_func(array_data[right_index],
                                                array_data[largest_index]):
        largest_index = right_index

    if largest_index != root_index:
        array_data[root_index], array_data[largest_index] =\
            array_data[largest_index], array_data[root_index]
        heapify(array_data, heap_size, largest_index, compare_func)


def heap_sort(array_data, compare_func):
    """
    Реализация пирамидальной сортировки (Heap Sort).

    Args:
        array_data (list): Массив транзакций для сортировки
        compare_func (function): Функция сравнения элементов
                                для определения порядка

    Returns:
        list: Отсортированный массив транзакций
    """
    if not array_data:
        return list()

    array_copy = copy_list(array_data)
    array_size = len(array_copy)

    # Построение максимальной кучи
    for index in range(array_size // 2 - 1, -1, -1):
        heapify(array_copy, array_size, index, compare_func)

    # Извлечение элементов из кучи
    for index in range(array_size - 1, 0, -1):
        array_copy[0], array_copy[index] = array_copy[index], array_copy[0]
        heapify(array_copy, index, 0, compare_func)

    return array_copy


def compare_income_by_date_desc_amount_desc(trans_1, trans_2):
    """
    Функция сравнения для сортировки поступлений:
    1. Дата по убыванию
    2. Сумма по убыванию

    Args:
        trans_1 (tuple): Первая транзакция для сравнения
        trans_2 (tuple): Вторая транзакция для сравнения

    Returns:
        bool: True если trans_1 должна идти позже
                trans_2 в отсортированном списке
    """
    date_1 = trans_1[0]
    date_2 = trans_2[0]
    amount1 = trans_1[4]
    amount2 = trans_2[4]

    if date_1 < date_2:
        return True
    elif date_1 > date_2:
        return False
    else:
        return amount1 < amount2


def compare_expenses_by_date_desc_contractor_asc_amount_desc\
                (trans_1, trans_2):
    """
    Функция сравнения для сортировки расходов по категории:
    1. Дата по убыванию
    2. Контрагент по возрастанию
    3. Сумма по убыванию

    Args:
        trans_1 (tuple): Первая транзакция для сравнения
        trans_2 (tuple): Вторая транзакция для сравнения

    Returns:
        bool: True если trans_1 должна идти позже
                trans_2 в отсортированном списке
    """
    date_1 = trans_1[0]
    date_2 = trans_2[0]
    contr1 = trans_1[5].lower()
    contr2 = trans_2[5].lower()
    amount1 = trans_1[4]
    amount2 = trans_2[4]

    if date_1 < date_2:
        return True
    elif date_1 > date_2:
        return False
    else:
        if contr1 > contr2:
            return True
        elif contr1 < contr2:
            return False
        else:
            return amount1 < amount2


def compare_expenses_by_time_range_amount_desc_contractor_asc\
                (trans_1, trans_2):
    """
    Функция сравнения для сортировки расходов по временному промежутку:
    1. Сумма по убыванию
    2. Контрагент по возрастанию
    3. Дата по убыванию (дополнительный ключ для однозначной сортировки)

    Args:
        trans_1 (tuple): Первая транзакция для сравнения
        trans_2 (tuple): Вторая транзакция для сравнения

    Returns:
        bool: True если trans_1 должна идти позже trans_2
                в отсортированном списке
    """
    amount1 = trans_1[4]
    amount2 = trans_2[4]
    contr1 = trans_1[5].lower()
    contr2 = trans_2[5].lower()
    date_1 = trans_1[0]
    date_2 = trans_2[0]

    # 1. Сумма по убыванию
    if amount1 < amount2:
        return True
    elif amount1 > amount2:
        return False
    else:
        # 2. Контрагент по возрастанию
        if contr1 > contr2:
            return True
        elif contr1 < contr2:
            return False
        else:
            # 3. Дата по убыванию
            return date_1 < date_2