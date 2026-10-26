"""Демонстрация: запуск командой ``python -m lab3``."""

import dataclasses
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from lab3.account import BankAccount
from lab3.filetool import TextFile
from lab3.json_encoder import JsonSerializer
from lab3.table_orm import Table
from lab3.vector import Vector


@dataclasses.dataclass
class Delivery:
    """Пример dataclass для сериализации."""

    number: int
    shipped: date
    weight: Decimal


def main() -> None:
    """Показать результат каждого задания варианта."""
    print("Средняя сложность")

    account = BankAccount("Ким Максим", "100.00")
    account.deposit("25.50")
    account.withdraw("0.50")
    print("Баланс счёта ->", account.balance)
    print("История операций ->", account.history)

    left = Vector([1, 2, 3])
    right = Vector([0.5, 0.5, 0.5])
    print("Сумма векторов ->", left + right)

    with tempfile.TemporaryDirectory() as directory:
        journal = TextFile(Path(directory) / "journal.txt")
        journal.write("первая строка\n")
        journal.append("вторая строка\n")
        print("Строки файла ->", journal.lines())
        print("Номера строк со словом «вторая» ->", journal.find("вторая"))

    print("Повышенная сложность")

    books = Table("books", ("id", "title", "year"), key="id")
    books.insert({"id": 1, "title": "Мастер и Маргарита", "year": 1967})
    books.insert({"id": 2, "title": "Пикник на обочине", "year": 1972})
    print(
        "Строки после 1970 ->",
        books.select(predicate=lambda row: row["year"] > 1970),
    )

    serializer = JsonSerializer(indent=2)
    delivery = Delivery(
        number=17,
        shipped=date(2026, 10, 26),
        weight=Decimal("3.75"),
    )
    print("JSON ->", serializer.dumps(delivery))


if __name__ == "__main__":
    main()
