"""Тесты мини-ORM (задание 7 повышенной сложности)."""

import unittest

from lab3.table_orm import Table, TableError


class TableTests(unittest.TestCase):
    """Проверки схемы, вставки и выборки строк."""

    def setUp(self) -> None:
        """Создать таблицу книг с уникальным ключом."""
        self.table = Table("books", ("id", "title", "year"), key="id")
        self.table.insert({"id": 1, "title": "Альфа", "year": 1960})
        self.table.insert({"id": 2, "title": "Бета", "year": 1975})

    def test_insert_returns_copy(self) -> None:
        """Изменение результата вставки не портит таблицу."""
        row = self.table.insert(
            {"id": 3, "title": "Гамма", "year": 2000}
        )
        row["title"] = "изменено"
        self.assertEqual(self.table.select(id=3)[0]["title"], "Гамма")

    def test_select_without_filters_returns_all(self) -> None:
        """Выборка без фильтров возвращает все строки по порядку."""
        self.assertEqual([row["id"] for row in self.table.select()], [1, 2])

    def test_select_filters_by_columns(self) -> None:
        """Фильтр по колонке возвращает только совпадения."""
        self.assertEqual(
            self.table.select(year=1975),
            [{"id": 2, "title": "Бета", "year": 1975}],
        )

    def test_select_accepts_predicate(self) -> None:
        """Предикат позволяет произвольное условие."""
        rows = self.table.select(predicate=lambda row: row["year"] < 1970)
        self.assertEqual([row["id"] for row in rows], [1])

    def test_unknown_column_is_rejected(self) -> None:
        """Неизвестная колонка в фильтре — ошибка схемы."""
        with self.assertRaises(TableError):
            self.table.select(author="кто-то")

    def test_insert_validates_columns(self) -> None:
        """Пропущенные и лишние колонки отклоняются."""
        with self.assertRaises(TableError):
            self.table.insert({"id": 3, "title": "Без года"})
        with self.assertRaises(TableError):
            self.table.insert(
                {"id": 3, "title": "Лишнее", "year": 2000, "x": 1}
            )

    def test_duplicate_key_is_rejected(self) -> None:
        """Значение ключа должно быть уникальным."""
        with self.assertRaises(TableError):
            self.table.insert({"id": 1, "title": "Дубль", "year": 2020})
        self.assertEqual(len(self.table), 2)

    def test_delete_reports_removed_rows(self) -> None:
        """Удаление возвращает количество строк."""
        self.assertEqual(self.table.delete(year=1960), 1)
        self.assertEqual(len(self.table), 1)

    def test_schema_validation(self) -> None:
        """Некорректная схема не создаётся."""
        with self.assertRaises(TableError):
            Table("", ("id",))
        with self.assertRaises(TableError):
            Table("t", ())
        with self.assertRaises(TableError):
            Table("t", ("id", "id"))
        with self.assertRaises(TableError):
            Table("t", ("id",), key="other")


if __name__ == "__main__":
    unittest.main()
