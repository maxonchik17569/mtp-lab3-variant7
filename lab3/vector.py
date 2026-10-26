"""Задание 7 (средняя сложность): перегрузка оператора сложения."""

from collections.abc import Iterable, Iterator


class Vector:
    """Вектор фиксированной размерности с покоординатным сложением."""

    def __init__(self, coordinates: Iterable[float]) -> None:
        """Создать вектор из последовательности чисел.

        Args:
            coordinates: координаты вектора, минимум одна.

        Raises:
            ValueError: если координат нет или они не числа.
        """
        values = tuple(coordinates)
        if not values:
            raise ValueError("vector must have at least one coordinate")
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"coordinate is not a number: {value!r}")
        self._coordinates = tuple(float(value) for value in values)

    @property
    def coordinates(self) -> tuple[float, ...]:
        """Координаты вектора."""
        return self._coordinates

    def __len__(self) -> int:
        """Размерность вектора."""
        return len(self._coordinates)

    def __getitem__(self, index: int) -> float:
        """Доступ к координате по индексу."""
        return self._coordinates[index]

    def __iter__(self) -> Iterator[float]:
        """Итерация по координатам."""
        return iter(self._coordinates)

    def __add__(self, other: object) -> "Vector":
        """Сложить два вектора одной размерности.

        Raises:
            TypeError: если второй операнд не вектор.
            ValueError: если размерности не совпадают.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("vectors must have the same dimension")
        return Vector(
            left + right
            for left, right in zip(self._coordinates, other)
        )

    def __eq__(self, other: object) -> bool:
        """Сравнить векторы по координатам."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self._coordinates == other._coordinates

    def __hash__(self) -> int:
        """Хеш по координатам, согласованный с равенством."""
        return hash(self._coordinates)

    def __repr__(self) -> str:
        """Читаемое представление вектора."""
        return f"Vector({list(self._coordinates)!r})"
