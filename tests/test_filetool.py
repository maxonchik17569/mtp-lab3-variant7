"""Тесты класса для работы с файлами (задание 9)."""

import tempfile
import unittest
from pathlib import Path

from lab3.filetool import TextFile


class TextFileTests(unittest.TestCase):
    """Проверки записи, чтения и поиска по файлу."""

    def setUp(self) -> None:
        """Создать временный каталог для каждого теста."""
        self._directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._directory.cleanup)
        self.path = Path(self._directory.name) / "notes.txt"
        self.file = TextFile(self.path)

    def test_write_and_read_round_trip(self) -> None:
        """Запись возвращает длину, чтение — тот же текст."""
        written = self.file.write("привет\nмир\n")
        self.assertEqual(written, len("привет\nмир\n"))
        self.assertEqual(self.file.read(), "привет\nмир\n")

    def test_append_adds_text_to_the_end(self) -> None:
        """Дописывание не стирает предыдущее содержимое."""
        self.file.write("первая\n")
        self.file.append("вторая\n")
        self.assertEqual(self.file.lines(), ["первая", "вторая"])

    def test_find_returns_line_numbers(self) -> None:
        """Поиск возвращает номера строк с единицы."""
        self.file.write("альфа\nбета\nальфа и гамма\n")
        self.assertEqual(self.file.find("альфа"), [1, 3])
        self.assertEqual(self.file.find("дельта"), [])

    def test_missing_file(self) -> None:
        """Отсутствующий файл не существует и не ищется."""
        self.assertFalse(self.file.exists)
        self.assertEqual(self.file.find("что угодно"), [])
        with self.assertRaises(FileNotFoundError):
            self.file.read()

    def test_encoding_is_configurable(self) -> None:
        """Кодировка влияет на байты файла."""
        windows = TextFile(self.path, encoding="cp1251")
        windows.write("ёж")
        self.assertEqual(self.path.read_bytes(), "ёж".encode("cp1251"))
        self.assertEqual(windows.read(), "ёж")


if __name__ == "__main__":
    unittest.main()
