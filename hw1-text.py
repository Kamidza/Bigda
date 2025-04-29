from typing import List
import string
from collections import Counter


def get_longest_diverse_words(file_path: str) -> List[str]:
    """Находит 10 самых длинных слов с наибольшим числом уникальных символов."""
    with open(file_path, encoding="utf-8") as f:
        words = set(word.strip(string.punctuation) for line in f for word in line.split())

    words = sorted(words, key=lambda w: (-len(set(w)), -len(w)))
    return words[:10]


def get_rarest_char(file_path: str) -> str:
    """Находит самый редкий символ в документе."""
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    counter = Counter(text)
    return min(counter, key=counter.get)


def count_punctuation_chars(file_path: str) -> int:
    """Считает количество знаков пунктуации в файле."""
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    return sum(1 for char in text if char in string.punctuation)


def count_non_ascii_chars(file_path: str) -> int:
    """Считает количество символов, не входящих в стандартную ASCII-таблицу."""
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    return sum(1 for char in text if ord(char) > 127)


def get_most_common_non_ascii_char(file_path: str) -> str:
    """Находит самый часто встречающийся не-ASCII символ в документе."""
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    counter = Counter(char for char in text if ord(char) > 127)
    return counter.most_common(1)[0][0] if counter else ""


if __name__ == "__main__":
    file_path = "/Users/blooomy/Desktop/data.txt"  # Укажите путь к вашему файлу

    print("10 самых длинных слов с наибольшим числом уникальных символов:")
    print(get_longest_diverse_words(file_path))

    print("\nСамый редкий символ в документе:")
    print(get_rarest_char(file_path))

    print("\nКоличество знаков пунктуации:")
    print(count_punctuation_chars(file_path))

    print("\nКоличество не-ASCII символов:")
    print(count_non_ascii_chars(file_path))

    print("\nСамый частый не-ASCII символ:")
    print(get_most_common_non_ascii_char(file_path))