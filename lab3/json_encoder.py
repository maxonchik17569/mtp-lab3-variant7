"""Задание 5 (повышенная сложность): сериализация объектов в JSON."""

import dataclasses
import json
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any


class SerializationError(TypeError):
    """Объект нельзя преобразовать в JSON-совместимое значение."""


class JsonSerializer:
    """Сериализатор, понимающий dataclass, даты, Decimal и множества.

    Класс рекурсивно обходит контейнеры и преобразует значения в
    типы, которые принимает модуль ``json``. Объект может сам
    описать себя методом ``to_json()`` или быть dataclass'ом.
    """

    def __init__(self, **json_options: Any) -> None:
        """Сохранить параметры для :func:`json.dumps`."""
        self._options = json_options

    def dumps(self, value: Any) -> str:
        """Сериализовать значение в JSON-строку.

        Args:
            value: произвольное поддерживаемое значение.

        Returns:
            JSON-строка в UTF-8-совместимом виде.

        Raises:
            SerializationError: если значение не сериализуется.
        """
        return json.dumps(
            self._convert(value),
            ensure_ascii=False,
            **self._options,
        )

    def loads(self, text: str) -> Any:
        """Разобрать JSON-строку обратно в обычные типы."""
        return json.loads(text)

    def _convert(self, value: Any) -> Any:
        """Рекурсивно привести значение к JSON-совместимому виду."""
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, (datetime, date, time)):
            return value.isoformat()
        if isinstance(value, Path):
            return str(value)
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return self._convert(dataclasses.asdict(value))
        if isinstance(value, dict):
            return {
                str(key): self._convert(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [self._convert(item) for item in value]
        if isinstance(value, (set, frozenset)):
            return [self._convert(item) for item in sorted(
                value, key=repr
            )]
        to_json = getattr(value, "to_json", None)
        if callable(to_json):
            return self._convert(to_json())
        raise SerializationError(
            f"cannot serialize object of type {type(value).__name__}"
        )
