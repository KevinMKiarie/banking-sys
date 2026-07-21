from typing import Dict, Optional
from banks.base_bank import BaseBank
from banks.mpesa import MPesaIntegration
from models.customer import Customer
from models.account import Account, AccountType


class BankingSystem:
    """
    Central orchestrator that manages multiple banks and M-Pesa.
    This is the single entry point your application talks to.
    """

    INTERBANK_FEE = 25.0  
    def __init__(self):
        self.__banks: Dict[str, BaseBank] = {}
        self.__mpesa = MPesaIntegration()

    @property
    def mpesa(self) -> MPesaIntegration:
        return self.__mpesa

    def register_bank(self, bank: BaseBank):
        self.__banks[bank.bank_code] = bank
        print(f"[System] Registered: {bank}")

    def get_bank(self, bank_code: str) -> Optional[BaseBank]:
        return self.__banks.get(bank_code)

    def list_banks(self):
        for code, bank in self.__banks.items():
            print(f"  [{code}] {bank.bank_name}")

    def interbank_transfer(
        self,
        from_bank_code: str,
        from_account: str,
        to_bank_code: str,
        to_account: str,
        amount: float,
    ):
        """
        Transfer between two different banks via PesaLink simulation.
        Debits sender (amount + flat fee)
        """
        sender_bank   = self.__banks.get(from_bank_code)
        receiver_bank = self.__banks.get(to_bank_code)

        if not sender_bank:
            raise LookupError(f"Bank code '{from_bank_code}' is not registered in the system")
        if not receiver_bank:
            raise LookupError(f"Bank code '{to_bank_code}' is not registered in the system")

        sender_bank.withdraw(
            from_account,
            amount + self.INTERBANK_FEE,
            f"Interbank transfer to {to_bank_code}/{to_account} (PesaLink fee: KES {self.INTERBANK_FEE})"
        )
        receiver_bank.deposit(
            to_account,
            amount,
            f"Interbank transfer from {from_bank_code}/{from_account}"
        )

        print(
            f"[System] Interbank transfer complete: KES {amount:,.2f} "
            f"from {sender_bank.bank_name} -> {receiver_bank.bank_name}. "
            f"Fee: KES {self.INTERBANK_FEE}"
        )

    def __repr__(self) -> str:
        return f"BankingSystem(banks={list(self.__banks.keys())})"
