"""Задание 9 (средняя сложность): класс для работы с файлами."""

from pathlib import Path


class TextFile:
    """Текстовый файл с чтением, записью и построчным доступом.

    Файл открывается на время каждой операции, поэтому объект можно
    спокойно хранить между вызовами и передавать в другие функции.
    """

    def __init__(self, path: str | Path, encoding: str = "utf-8") -> None:
        """Запомнить путь и кодировку.

        Args:
            path: путь к файлу; каталог должен существовать.
            encoding: кодировка текста.
        """
        self.path = Path(path)
        self.encoding = encoding

    @property
    def exists(self) -> bool:
        """Признак того, что файл уже создан."""
        return self.path.is_file()

    def write(self, text: str) -> int:
        """Перезаписать файл текстом.

        Args:
            text: новое содержимое файла.

        Returns:
            Количество записанных символов.
        """
        self.path.write_text(text, encoding=self.encoding)
        return len(text)

    def append(self, text: str) -> None:
        """Дописать текст в конец файла."""
        with self.path.open("a", encoding=self.encoding) as stream:
            stream.write(text)

    def read(self) -> str:
        """Прочитать весь файл.

        Raises:
            FileNotFoundError: если файла ещё нет.
        """
        return self.path.read_text(encoding=self.encoding)

    def lines(self) -> list[str]:
        """Вернуть строки файла без символов перевода строки."""
        return self.read().splitlines()

    def find(self, needle: str) -> list[int]:
        """Найти номера строк, содержащих подстроку.

        Args:
            needle: искомая подстрока.

        Returns:
            Номера строк (с единицы); пустой список, если совпадений
            нет или файл отсутствует.
        """
        if not self.exists:
            return []
        return [
            number
            for number, line in enumerate(self.lines(), start=1)
            if needle in line
        ]
