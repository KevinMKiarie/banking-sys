from abc import ABC, abstractmethod
from typing import Optional

from models.account import Account, AccountType
from models.customer import Customer
from models.transaction import Transaction


class BaseBank(ABC):
    """
    Abstract base class — a contract every Kenyan bank must honour.
    Any class that inherits this MUST implement all @abstractmethod
    methods or Python raises TypeError at instantiation time.
    """

    def __init__(self, bank_name: str, bank_code: str, swift_code: str):
        self._bank_name = bank_name
        self._bank_code = bank_code
        self._swift_code = swift_code
        self._customers: dict = {}  # national_id -> Customer
        self._accounts: dict = {}  # account_number -> Account

    @property
    def bank_name(self) -> str:
        return self._bank_name

    @property
    def bank_code(self) -> str:
        return self._bank_code

    # ------------------------------------------------------------------
    # Abstract methods — every subclass must provide its own version
    # ------------------------------------------------------------------

    @abstractmethod
    def open_account(
        self, customer: Customer, account_type: AccountType, initial_deposit: float
    ) -> Account:
        pass

    @abstractmethod
    def deposit(
        self, account_number: str, amount: float, description: str = ""
    ) -> Transaction:
        pass

    @abstractmethod
    def withdraw(
        self, account_number: str, amount: float, description: str = ""
    ) -> Transaction:
        pass

    @abstractmethod
    def transfer(
        self, from_account: str, to_account: str, amount: float
    ) -> Transaction:
        pass

    @abstractmethod
    def get_balance(self, account_number: str) -> float:
        pass

    # ------------------------------------------------------------------
    # Shared concrete helpers — inherited as-is by all subclasses
    # ------------------------------------------------------------------

    def get_account(self, account_number: str) -> Optional[Account]:
        return self._accounts.get(account_number)

    def get_customer(self, national_id: str) -> Optional[Customer]:
        return self._customers.get(national_id)

    def _generate_account_number(self, prefix: str) -> str:
        import random

        digits = "".join([str(random.randint(0, 9)) for _ in range(8)])
        return f"{prefix}{digits}"

    def _validate_account(self, account_number: str) -> Account:
        """Reused by every subclass to guard operations before they run."""
        account = self._accounts.get(account_number)
        if not account:
            raise LookupError(
                f"Account {account_number} not found at {self._bank_name}"
            )
        if not account.is_active:
            raise PermissionError(f"Account {account_number} is inactive")
        return account

    def __repr__(self) -> str:
        return f"{self._bank_name} (Code: {self._bank_code}, SWIFT: {self._swift_code})"
