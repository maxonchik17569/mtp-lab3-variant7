"""Задание 7 (повышенная сложность): мини-ORM с классом Table."""

from collections.abc import Callable, Iterable, Mapping
from typing import Any


class TableError(ValueError):
    """Ошибка схемы или операции над таблицей."""


class Table:
    """Таблица в памяти со схемой, вставкой и выборкой строк.

    Строка — обычный словарь. Таблица проверяет имена колонок,
    обязательность значений и уникальность ключа, но не пытается
    быть полноценной СУБД.
    """

    def __init__(
        self,
        name: str,
        columns: Iterable[str],
        key: str | None = None,
    ) -> None:
        """Объявить таблицу.

        Args:
            name: имя таблицы.
            columns: имена колонок в порядке объявления.
            key: необязательная колонка с уникальными значениями.

        Raises:
            TableError: если имя пустое, колонок нет, имена
                повторяются или ключ отсутствует среди колонок.
        """
        if not name.strip():
            raise TableError("table name must not be empty")
        declared = tuple(columns)
        if not declared:
            raise TableError("table must have at least one column")
        if len(set(declared)) != len(declared):
            raise TableError("column names must be unique")
        if key is not None and key not in declared:
            raise TableError(f"unknown key column: {key}")
        self.name = name
        self.columns = declared
        self.key = key
        self._rows: list[dict[str, Any]] = []

    def __len__(self) -> int:
        """Количество строк в таблице."""
        return len(self._rows)

    def insert(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Вставить строку.

        Args:
            row: значения по именам колонок; все колонки обязательны.

        Returns:
            Копия вставленной строки.

        Raises:
            TableError: если колонки неизвестны, пропущены или
                значение ключа уже существует.
        """
        unknown = set(row) - set(self.columns)
        if unknown:
            raise TableError(f"unknown columns: {sorted(unknown)}")
        missing = set(self.columns) - set(row)
        if missing:
            raise TableError(f"missing columns: {sorted(missing)}")
        stored = {column: row[column] for column in self.columns}
        if self.key is not None:
            existing = self.select(**{self.key: stored[self.key]})
            if existing:
                raise TableError(
                    f"duplicate key {self.key}={stored[self.key]!r}"
                )
        self._rows.append(stored)
        return dict(stored)

    def select(
        self,
        predicate: Callable[[Mapping[str, Any]], bool] | None = None,
        **filters: Any,
    ) -> list[dict[str, Any]]:
        """Выбрать строки по равенству колонок и/или предикату.

        Args:
            predicate: необязательная функция-фильтр.
            **filters: пары «колонка=значение».

        Returns:
            Список копий подходящих строк в порядке вставки.

        Raises:
            TableError: если фильтр ссылается на неизвестную колонку.
        """
        unknown = set(filters) - set(self.columns)
        if unknown:
            raise TableError(f"unknown columns: {sorted(unknown)}")
        result: list[dict[str, Any]] = []
        for row in self._rows:
            if any(row[column] != value for column, value in filters.items()):
                continue
            if predicate is not None and not predicate(row):
                continue
            result.append(dict(row))
        return result

    def delete(self, **filters: Any) -> int:
        """Удалить строки, подходящие под фильтры.

        Returns:
            Количество удалённых строк.
        """
        keep: list[dict[str, Any]] = []
        removed = 0
        for row in self._rows:
            matched = all(
                row[column] == value for column, value in filters.items()
            )
            if matched:
                removed += 1
            else:
                keep.append(row)
        self._rows = keep
        return removed

    def __repr__(self) -> str:
        """Читаемое представление таблицы."""
        return f"Table(name={self.name!r}, rows={len(self._rows)})"
