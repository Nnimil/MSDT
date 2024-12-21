import json
import hashlib
from typing import List
import csv
from validator import Validator  # Убедитесь, что Validator определен

CSV_PATH = "./21.csv"  # Укажите путь к вашему CSV-файлу
JSON_PATH = "result.json"
OPTION = 21  # Укажите ваш вариант

def get_numbers_id_with_wrong_data(csv_file_path: str) -> list[int]:
    """Получить номера строк с ошибками из CSV-файла."""
    numbers_id_with_wrong_data = []
    validator = Validator()  # Создаем экземпляр валидатора
    with open(csv_file_path, newline='', encoding="utf-16") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row_id, row in enumerate(reader):
            for pattern, data in row.items():
                if not validator.validate_data(pattern, data):
                    numbers_id_with_wrong_data.append(row_id - 1)  # Корректируем индекс
    return numbers_id_with_wrong_data

def calculate_checksum(row_numbers: List[int]) -> str:
    """Вычислить контрольную сумму."""
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()

def serialize_result(variant: int, checksum: str) -> None:
    """Записать результат в JSON."""
    result = {
        "variant": variant,
        "checksum": checksum
    }
    with open(JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file)

def main():
    """Основная функция."""
    numbers_id_with_wrong_data = get_numbers_id_with_wrong_data(CSV_PATH)
    check_sum = calculate_checksum(numbers_id_with_wrong_data)
    serialize_result(OPTION, check_sum)

if __name__ == "__main__":
    main()
