"""
Модуль для хранения данных бюджета.
Отвечает за сохранение и загрузку транзакций в/из файла.
"""

data_file = "budget_data.txt"


def save_transactions(transactions):
    """
    Сохраняет транзакции в текстовый файл.

    Args:
        transactions (list): Список транзакций для сохранения
    """
    try:
        file_handler = open(data_file, 'w', encoding='utf-8')
        try:
            for transaction in transactions:
                # Преобразуем кортеж в строку:
                # дата|время|направление|категория|сумма|контрагент
                (date_str, time_str, direction_str,
                 category_str, amount_val, contractor_str) = transaction
                line = (f"{date_str}|{time_str}|{direction_str}"
                        f"|{category_str}|{amount_val}|{contractor_str}")
                file_handler.write(line + '\n')
            print(f" Данные сохранены в файл '{data_file}'")
            return True
        finally:
            file_handler.close()
    except Exception as error:
        print(f"Ошибка при сохранении данных: {error}")
        return False


def load_transactions():
    """
    Загружает транзакции из текстового файла.

    Returns:
        list: Список загруженных транзакций
    """
    transactions_list = list()
    
    try:
        file_handler = open(data_file, 'r', encoding='utf-8')
    except FileNotFoundError:
        print(f"Файл данных '{data_file}' не найден."
              f" Будет создан новый при сохранении.")
        return transactions_list
    
    try:
        line_number = 0
        while True:
            line_content = file_handler.readline()
            if not line_content:
                break
            
            line_number += 1
            line_content = line_content.strip()
            
            if not line_content:
                continue
            
            parts = line_content.split('|')
            if len(parts) != 6:
                print(f"Предупреждение: строка {line_number} имеет "
                      f"неверный формат, пропущена")
                continue
            
            try:
                date_part = parts[0]
                time_part = parts[1]
                direction_part = parts[2]
                category_part = parts[3]
                amount_part = float(parts[4])
                contractor_part = parts[5]
                
                transaction_tuple = (date_part, time_part, direction_part,
                                     category_part, amount_part, contractor_part)
                transactions_list.append(transaction_tuple)
            except ValueError:
                print(f"Предупреждение: ошибка преобразования данных"
                      f" в строке {line_number}, пропущена")
                continue
    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
    finally:
        file_handler.close()
    
    return transactions_list