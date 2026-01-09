"""
Модуль отображения данных бюджета.
Отвечает за форматированный вывод транзакций в консоль.
"""

def display_transaction(transaction, index=None):
    """
    Отображает одну транзакцию в читаемом формате.

    Args:
        transaction (tuple): Кортеж с данными транзакции в формате (дата, время,
                            направление, категория, сумма, контрагент)
        index (int, optional): Номер транзакции для нумерации в списке.
                                Defaults to None.
    """
    date, time, direction, category, amount, contractor = transaction

    if index is not None:
        prefix = f"{index:3}. "
    else:
        prefix = "     "

    direction_symbol = "+" if direction == "приход" else "-"
    print(f"{prefix}{date} {time} | {direction_symbol}"
          f" {amount:8} руб. | {category:12} | {contractor}")


def display_transactions(transactions, title="Список транзакций"):
    """
    Отображает список транзакций с заголовком.

    Args:
        transactions (list): Список транзакций для отображения
        title (str, optional): Заголовок списка.
                                Defaults to "Список транзакций".
    """
    if not transactions:
        print("Нет транзакций для отображения.")
        return

    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")

    for index, transaction in enumerate(transactions, 1):
        display_transaction(transaction, index)

    print(f"{'=' * 60}")
    print(f"Всего: {len(transactions)} транзакций")