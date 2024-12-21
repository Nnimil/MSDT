import re

class Validator:
    def __init__(self):
        self.patterns = {
            'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'telephone': r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
            'http_status_message': r'^\d{3} [A-Za-z ]+$',
            'height': r'^\d+\.\d{2}$',
            'snils': r'^\d{11}$',
            'inn': r'^\d{12}$',
            'passport': r'^\d{2} \d{2} \d{6}$',
            'identifier': r'^\d{2}-\d{2}/\d{2}$',
            'ip_v4': r'^(\d{1,3}\.){3}\d{1,3}$',
            'occupation': r'^[\w\s\-]+$'
        }

    def validate_data(self, pattern: str, data: str) -> bool:
        """Проверить данные на соответствие регулярному выражению."""
        if pattern not in self.patterns:
            return False
        regex = re.compile(self.patterns[pattern])
        if pattern == 'ip_v4':
            # Дополнительная проверка для IPv4
            return regex.match(data) and all(0 <= int(octet) <= 255 for octet in data.split('.'))
        if pattern == 'height':
            # Дополнительная проверка для роста
            return regex.match(data) and 0.50 <= float(data) <= 2.50
        return bool(regex.match(data))
