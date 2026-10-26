"""Задание 3 (средняя сложность): класс банковского счёта."""

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


class AccountError(ValueError):
    """Базовое исключение для операций со счётом."""


class InsufficientFunds(AccountError):
    """Попытка снять сумму больше текущего остатка."""

    def __init__(self, balance: Decimal, amount: Decimal) -> None:
        """Сохранить остаток и запрошенную сумму для сообщения."""
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"insufficient funds: balance={balance}, requested={amount}"
        )


def to_money(value: object) -> Decimal:
    """Привести значение к сумме с двумя знаками после запятой."""
    try:
        amount = Decimal(str(value))
    except Exception as exc:  # noqa: BLE001 - любое нечисловое значение
        raise AccountError(f"invalid amount: {value!r}") from exc
    if not amount.is_finite():
        raise AccountError("amount must be finite")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


class BankAccount:
    """Счёт владельца с пополнением, снятием и историей операций."""

    def __init__(self, owner: str, balance: object = 0) -> None:
        """Открыть счёт с начальным остатком.

        Args:
            owner: имя владельца, непустая строка.
            balance: начальный остаток, неотрицательная сумма.

        Raises:
            AccountError: если имя пустое или остаток отрицателен.
        """
        if not owner.strip():
            raise AccountError("owner must not be empty")
        start = to_money(balance)
        if start < 0:
            raise AccountError("initial balance must be non-negative")
        self.owner = owner.strip()
        self._balance = start
        self._history: list[tuple[str, Decimal]] = []

    @property
    def balance(self) -> Decimal:
        """Текущий остаток счёта."""
        return self._balance

    @property
    def history(self) -> tuple[tuple[str, Decimal], ...]:
        """Неизменяемая копия списка операций."""
        return tuple(self._history)

    def deposit(self, amount: object) -> Decimal:
        """Пополнить счёт на положительную сумму.

        Args:
            amount: сумма пополнения.

        Returns:
            Остаток после операции.

        Raises:
            AccountError: если сумма не положительна.
        """
        value = to_money(amount)
        if value <= 0:
            raise AccountError("deposit amount must be positive")
        self._balance += value
        self._history.append(("deposit", value))
        return self._balance

    def withdraw(self, amount: object) -> Decimal:
        """Снять положительную сумму, не превышающую остаток.

        Args:
            amount: сумма снятия.

        Returns:
            Остаток после операции.

        Raises:
            AccountError: если сумма не положительна.
            InsufficientFunds: если сумма больше остатка; баланс при
                этом не меняется.
        """
        value = to_money(amount)
        if value <= 0:
            raise AccountError("withdraw amount must be positive")
        if value > self._balance:
            raise InsufficientFunds(self._balance, value)
        self._balance -= value
        self._history.append(("withdraw", value))
        return self._balance

    def __repr__(self) -> str:
        """Читаемое представление счёта."""
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"
