
import re

# Разрешённые символы: латиница, кириллица, цифры, пробел, -, +, ,, ., (, )
ALLOWED_PATTERN = re.compile(r'^[A-Za-z\u0400-\u04FF0-9 \-\+,\.\(\)]+$')
ALLOWED_CHARS = set(
    # Русские буквы
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    # Украинские буквы
    'ІіЇїЄєҐґ'
    # Латиница
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    '0123456789-+,.() '
)

def check_allowed_characters(text):
    """
    Проверяет, содержит ли текст только разрешённые символы.
    Если есть спецсимволы — возвращает строку с выделением этих символов.
    """
    special_chars = [ch for ch in text if ch not in ALLOWED_CHARS]
    if not special_chars:
        return True, text
    # Выделяем спецсимволы, например, оборачиваем в [! ... !]
    highlighted = ''
    for ch in text:
        if ch in ALLOWED_CHARS:
            highlighted += ch
        else:
            highlighted += f'[!{ch}!]'
    return False, f'В тексте присутствует спецсимвол(ы): {", ".join(set(special_chars))}\n{highlighted}'
