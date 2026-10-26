"""Тесты перегрузки оператора сложения (задание 7)."""

import unittest

from lab3.vector import Vector


class VectorTests(unittest.TestCase):
    """Проверки сложения, равенства и валидации векторов."""

    def test_addition_is_coordinate_wise(self) -> None:
        """Сложение складывает соответствующие координаты."""
        result = Vector([1, 2, 3]) + Vector([0.5, 0.5, 0.5])
        self.assertEqual(result, Vector([1.5, 2.5, 3.5]))

    def test_dimension_mismatch_raises(self) -> None:
        """Векторы разной длины складывать нельзя."""
        with self.assertRaises(ValueError):
            Vector([1, 2]) + Vector([1])

    def test_non_vector_operand_raises_type_error(self) -> None:
        """Сложение с числом или списком не поддерживается."""
        with self.assertRaises(TypeError):
            Vector([1]) + [2]

    def test_equality_and_hash_use_coordinates(self) -> None:
        """Равные векторы равны и имеют одинаковый хеш."""
        first = Vector([1, 2])
        second = Vector([1.0, 2.0])
        self.assertEqual(first, second)
        self.assertEqual(hash(first), hash(second))
        self.assertNotEqual(first, Vector([2, 1]))

    def test_coordinates_are_immutable(self) -> None:
        """Координаты доступны только для чтения."""
        vector = Vector([1, 2])
        self.assertEqual(vector.coordinates, (1.0, 2.0))
        with self.assertRaises(AttributeError):
            vector.coordinates = (3, 4)

    def test_invalid_coordinates_are_rejected(self) -> None:
        """Пустой вектор и нечисловые координаты отклоняются."""
        with self.assertRaises(ValueError):
            Vector([])
        with self.assertRaises(ValueError):
            Vector([1, "два"])
        with self.assertRaises(ValueError):
            Vector([True])


if __name__ == "__main__":
    unittest.main()
