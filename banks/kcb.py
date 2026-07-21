from banks.base_bank import BaseBank
from models.customer import Customer
from models.account import Account, AccountType
from models.transaction import Transaction


class KCBBank(BaseBank):
    """Kenya Commercial Bank — KCB Group PLC"""

    TRANSFER_FEE_PERCENT  = 0.002      # 0.2% on every internal transfer
    DAILY_WITHDRAWAL_LIMIT = 500_000   # KES 500,000

    def __init__(self):
        super().__init__(
            bank_name="KCB Bank Kenya",
            bank_code="01",
            swift_code="KCBLKENX"
        )

    def open_account(self, customer: Customer, account_type: AccountType, initial_deposit: float) -> Account:
        if customer.national_id in self._customers:
            raise ValueError(f"Customer {customer.national_id} already registered at KCB")

        min_opening = Account.MINIMUM_BALANCE[account_type]
        if initial_deposit < min_opening:
            raise ValueError(
                f"Minimum opening deposit for {account_type.value} is KES {min_opening:,.2f}"
            )

        account_number = self._generate_account_number(prefix="1316")
        account = Account(account_number, customer.national_id, account_type, initial_deposit)

        self._customers[customer.national_id] = customer
        self._accounts[account_number] = account

        print(f"[KCB] Account opened: {account_number} for {customer.full_name}")
        return account

    def deposit(self, account_number: str, amount: float, description: str = "Cash deposit") -> Transaction:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        account = self._validate_account(account_number)
        txn = account._credit(amount, description)
        print(f"[KCB] Deposited KES {amount:,.2f} to {account_number}. Balance: KES {account.balance:,.2f}")
        return txn

    def withdraw(self, account_number: str, amount: float, description: str = "Cash withdrawal") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.DAILY_WITHDRAWAL_LIMIT:
            raise ValueError(
                f"Amount exceeds KCB daily withdrawal limit of KES {self.DAILY_WITHDRAWAL_LIMIT:,.2f}"
            )
        account = self._validate_account(account_number)
        txn = account._debit(amount, description)
        print(f"[KCB] Withdrew KES {amount:,.2f} from {account_number}. Balance: KES {account.balance:,.2f}")
        return txn

    def transfer(self, from_account: str, to_account: str, amount: float) -> Transaction:
        fee = round(amount * self.TRANSFER_FEE_PERCENT, 2)
        total_debit = amount + fee

        sender   = self._validate_account(from_account)
        receiver = self._validate_account(to_account)

        sender._debit(total_debit, f"Transfer to {to_account} (fee: KES {fee})")
        txn = receiver._credit(amount, f"Transfer from {from_account}")

        print(f"[KCB] Transferred KES {amount:,.2f}: {from_account} -> {to_account}. Fee: KES {fee}")
        return txn

    def get_balance(self, account_number: str) -> float:
        return self._validate_account(account_number).balance
