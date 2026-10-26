# Лабораторная работа №3

Ким Максим Сергеевич, группа 221341, вариант 7, лабораторная №3.

Тема: объектно-ориентированное программирование на Python — классы,
инкапсуляция, перегрузка операторов, property, мини-ORM.

## Задания варианта

**Средняя сложность:**

- №7 — перегрузка оператора `+` (`lab3/vector.py`)
- №9 — класс для работы с файлами (`lab3/filetool.py`)
- №3 — класс «Банковский счёт» с пополнением и снятием
  (`lab3/account.py`)

**Повышенная сложность:**

- №7 — мини-ORM: класс «Таблица» с методами `insert` и `select`
  (`lab3/table_orm.py`)
- №5 — класс для сериализации объектов в JSON
  (`lab3/json_encoder.py`)

## Клонирование

```bash
git clone https://github.com/maxonchik17569/mtp-lab3-variant7.git
cd mtp-lab3-variant7
```

## Запуск

```bash
uv run python -m lab3
```

## Проверки

```bash
uv run python -m unittest discover -s tests -v
uv run python -m compileall -q lab3 tests
uv run --with flake8 flake8 lab3 tests
```

Подробное описание решений — в `docs/report.md`.

## Структура репозитория

```text
lab3/                 # пакет с модулями по одному на задание
  account.py          # банковский счёт
  filetool.py         # текстовый файл
  vector.py           # перегрузка оператора сложения
  table_orm.py        # мини-ORM
  json_encoder.py     # сериализация в JSON
  __main__.py         # демонстрация всех заданий
tests/                # unittest-тесты по модулям
docs/report.md        # отчёт по работе
```

## Требования

- Python 3.13 или новее.
- [uv](https://docs.astral.sh/uv/) для запуска без ручной установки
  зависимостей.
- `flake8` ставится автоматически командой `uv run --with flake8`.
