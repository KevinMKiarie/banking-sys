from datetime import datetime
from enum import Enum
import uuid


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    MPESA_IN = "MPESA_IN"
    MPESA_OUT = "MPESA_OUT"


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class Transaction:
    def __init__(
        self,
        transaction_type: TransactionType,
        amount: float,
        account_number: str,
        description: str = "",
        reference: str = None,
    ):
        self.__id = str(uuid.uuid4())[:8].upper()
        self.__type = transaction_type
        self.__amount = amount
        self.__account_number = account_number
        self.__description = description
        self.__reference = reference or self.__id
        self.__timestamp = datetime.now()
        self.__status = TransactionStatus.PENDING

    @property
    def id(self) -> str:
        return self.__id

    @property
    def type(self) -> TransactionType:
        return self.__type

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def account_number(self) -> str:
        return self.__account_number

    @property
    def description(self) -> str:
        return self.__description

    @property
    def reference(self) -> str:
        return self.__reference

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def status(self) -> TransactionStatus:
        return self.__status

    def mark_completed(self):
        if self.__status != TransactionStatus.PENDING:
            raise RuntimeError("Transaction already finalized")
        self.__status = TransactionStatus.COMPLETED

    def mark_failed(self, reason: str = ""):
        if self.__status != TransactionStatus.PENDING:
            raise RuntimeError("Transaction already finalized")
        self.__status = TransactionStatus.FAILED
        self.__description += f" [FAILED: {reason}]"

    def __repr__(self) -> str:
        return (
            f"Transaction({self.__id} | {self.__type.value} | "
            f"KES {self.__amount:,.2f} | {self.__status.value})"
        )
