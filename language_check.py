

# Словари похожих символов между кириллицей (включая украинские буквы) и латиницей
CYR_TO_LAT = {
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'Ё': 'E',
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x', 'ё': 'e',
    # Украинские
    'І': 'I', 'і': 'i', 'Ї': 'Yi', 'ї': 'yi', 'Є': 'Ye', 'є': 'ye', 'Ґ': 'G', 'ґ': 'g',
}
LAT_TO_CYR = {
    'A': 'А', 'B': 'В', 'E': 'Е', 'K': 'К', 'M': 'М', 'H': 'Н', 'O': 'О', 'P': 'Р', 'C': 'С', 'T': 'Т', 'X': 'Х',
    'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с', 'y': 'у', 'x': 'х',
    # Украинские
    'I': 'І', 'i': 'і'
}

import re

def detect_language(text):
    # Добавляем украинские буквы к диапазону кириллицы
    cyrillic_pattern = r'[\u0400-\u04FF\u0456\u0457\u0491\u0406\u0407\u0490]'
    cyrillic_count = len(re.findall(cyrillic_pattern, text))
    latin_count = len(re.findall(r'[A-Za-z]', text))
    if cyrillic_count > latin_count:
        return 'cyrillic'
    elif latin_count > cyrillic_count:
        return 'latin'
    else:
        return 'unknown'

def fix_mixed_letters(text):
    lang = detect_language(text)
    if lang == 'cyrillic':
        # Заменяем латинские буквы на кириллические
        return ''.join(LAT_TO_CYR.get(ch, ch) for ch in text)
    elif lang == 'latin':
        # Заменяем кириллические буквы на латинские
        return ''.join(CYR_TO_LAT.get(ch, ch) for ch in text)
    else:
        return text
