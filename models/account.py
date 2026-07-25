from enum import Enum
from typing import List

from models.transaction import Transaction, TransactionStatus, TransactionType


class AccountType(Enum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"
    FIXED = "FIXED_DEPOSIT"


class Account:
    MINIMUM_BALANCE = {
        AccountType.SAVINGS: 1000.0,
        AccountType.CURRENT: 5000.0,
        AccountType.FIXED: 10000.0,
    }

    def __init__(
        self,
        account_number: str,
        owner_id: str,
        account_type: AccountType,
        opening_balance: float = 0.0,
    ):
        self.__account_number = account_number
        self.__owner_id = owner_id
        self.__account_type = account_type
        self.__balance = 0.0
        self.__transactions: List[Transaction] = []
        self.__is_active = True

        if opening_balance > 0:
            self._credit(opening_balance, "Opening balance")

    def _credit(self, amount: float, description: str) -> Transaction:
        txn = Transaction(
            TransactionType.DEPOSIT, amount, self.__account_number, description
        )
        self.__balance += amount
        self.__transactions.append(txn)
        txn.mark_completed()
        return txn

    def _debit(self, amount: float, description: str) -> Transaction:
        min_bal = self.MINIMUM_BALANCE[self.__account_type]
        if self.__balance - amount < min_bal:
            raise ValueError(
                f"Insufficient funds. Balance after transaction would fall below "
                f"minimum KES {min_bal:,.2f} for {self.__account_type.value} account."
            )
        txn = Transaction(
            TransactionType.WITHDRAWAL, amount, self.__account_number, description
        )
        self.__balance -= amount
        self.__transactions.append(txn)
        txn.mark_completed()
        return txn

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def owner_id(self) -> str:
        return self.__owner_id

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def account_type(self) -> AccountType:
        return self.__account_type

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def transaction_history(self) -> List[Transaction]:
        return list(self.__transactions)

    def deactivate(self):
        self.__is_active = False

    def get_mini_statement(self, last_n: int = 5) -> str:
        lines = [
            f"Account: {self.__account_number} | Balance: KES {self.__balance:,.2f}"
        ]
        for txn in self.__transactions[-last_n:]:
            lines.append(
                f"  {txn.timestamp.strftime('%d/%m/%Y %H:%M')} | "
                f"{txn.type.value:<12} | KES {txn.amount:>10,.2f} | {txn.description}"
            )
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Account({self.__account_number} | {self.__account_type.value} | KES {self.__balance:,.2f})"
