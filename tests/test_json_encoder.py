"""Тесты сериализации объектов в JSON (задание 5 повышенной сложности)."""

import dataclasses
import json
import unittest
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from lab3.json_encoder import JsonSerializer, SerializationError


@dataclasses.dataclass
class Order:
    """Пример dataclass с разными типами полей."""

    number: int
    created: date
    price: Decimal
    tags: set[str]


class Point:
    """Класс, который сам описывает своё JSON-представление."""

    def __init__(self, x: int, y: int) -> None:
        """Сохранить координаты точки."""
        self.x = x
        self.y = y

    def to_json(self) -> dict[str, int]:
        """Вернуть JSON-совместимый словарь."""
        return {"x": self.x, "y": self.y}


class JsonSerializerTests(unittest.TestCase):
    """Проверки преобразования поддерживаемых типов."""

    def setUp(self) -> None:
        """Создать сериализатор без отступов."""
        self.serializer = JsonSerializer()

    def test_dataclass_is_serialized(self) -> None:
        """dataclass разбирается на поля и кодируется в JSON."""
        value = Order(
            number=7,
            created=date(2026, 10, 26),
            price=Decimal("19.90"),
            tags={"новый", "срочный"},
        )
        decoded = json.loads(self.serializer.dumps(value))
        self.assertEqual(decoded["number"], 7)
        self.assertEqual(decoded["created"], "2026-10-26")
        self.assertEqual(decoded["price"], "19.90")
        self.assertEqual(sorted(decoded["tags"]), ["новый", "срочный"])

    def test_datetime_and_path_are_strings(self) -> None:
        """Дата-время и Path превращаются в строки."""
        moment = datetime(2026, 10, 26, 12, 30, 15)
        self.assertEqual(
            self.serializer.dumps({"at": moment}),
            '{"at": "2026-10-26T12:30:15"}',
        )
        self.assertEqual(
            self.serializer.dumps({"path": Path("docs/report.md")}),
            '{"path": "docs/report.md"}',
        )

    def test_object_with_to_json_method(self) -> None:
        """Объект с методом to_json сериализуется через него."""
        decoded = json.loads(self.serializer.dumps(Point(2, 3)))
        self.assertEqual(decoded, {"x": 2, "y": 3})

    def test_nested_containers_and_non_string_keys(self) -> None:
        """Вложенные структуры обходятся рекурсивно, ключи — строки."""
        payload = {"rows": [{"id": 1, "values": (1, 2, 3)}], 5: "пять"}
        decoded = json.loads(self.serializer.dumps(payload))
        self.assertEqual(decoded["rows"][0]["values"], [1, 2, 3])
        self.assertEqual(decoded["5"], "пять")

    def test_cyrillic_is_not_escaped(self) -> None:
        """ensure_ascii=False сохраняет кириллицу читаемой."""
        self.assertEqual(
            self.serializer.dumps({"имя": "ёж"}),
            '{"имя": "ёж"}',
        )

    def test_loads_round_trip(self) -> None:
        """loads разбирает строку обратно в обычный словарь."""
        since = self.serializer.dumps({"ok": True})
        self.assertEqual(self.serializer.loads(since), {"ok": True})

    def test_unsupported_object_raises(self) -> None:
        """Объект без поддержки приводит к SerializationError."""

        class Anonymous:
            pass

        with self.assertRaises(SerializationError):
            self.serializer.dumps({"value": Anonymous()})


if __name__ == "__main__":
    unittest.main()
