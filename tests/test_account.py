"""Тесты банковского счёта (задание 3)."""

import unittest
from decimal import Decimal

from lab3.account import AccountError, BankAccount, InsufficientFunds


class BankAccountTests(unittest.TestCase):
    """Проверки пополнения, снятия и истории операций."""

    def test_initial_balance_is_quantized(self) -> None:
        """Начальный остаток приводится к двум знакам."""
        account = BankAccount("Ким Максим", "10.005")
        self.assertEqual(account.balance, Decimal("10.01"))

    def test_deposit_and_withdraw_change_balance(self) -> None:
        """Пополнение и снятие корректно меняют остаток."""
        account = BankAccount("Ким Максим", 100)
        self.assertEqual(account.deposit("25.50"), Decimal("125.50"))
        self.assertEqual(account.withdraw("0.50"), Decimal("125.00"))
        self.assertEqual(
            account.history,
            (("deposit", Decimal("25.50")),
             ("withdraw", Decimal("0.50"))),
        )

    def test_insufficient_funds_keeps_balance(self) -> None:
        """Неудачное снятие не меняет остаток и историю."""
        account = BankAccount("Ким Максим", 10)
        with self.assertRaises(InsufficientFunds) as caught:
            account.withdraw(20)
        self.assertEqual(caught.exception.balance, Decimal("10.00"))
        self.assertEqual(account.balance, Decimal("10.00"))
        self.assertEqual(account.history, ())

    def test_non_positive_amounts_are_rejected(self) -> None:
        """Нулевые и отрицательные суммы недопустимы."""
        account = BankAccount("Ким Максим", 10)
        for amount in (0, "-1", "abc", None):
            with self.subTest(amount=amount):
                with self.assertRaises(AccountError):
                    account.deposit(amount)
        with self.assertRaises(AccountError):
            account.withdraw("-5")

    def test_negative_initial_balance_and_empty_owner(self) -> None:
        """Отрицательный старт и пустое имя отклоняются."""
        with self.assertRaises(AccountError):
            BankAccount("Ким Максим", -1)
        with self.assertRaises(AccountError):
            BankAccount("   ")

    def test_repr_contains_owner_and_balance(self) -> None:
        """Представление содержит владельца и остаток."""
        text = repr(BankAccount("Ким Максим", 5))
        self.assertIn("Ким Максим", text)
        self.assertIn("5.00", text)


if __name__ == "__main__":
    unittest.main()
