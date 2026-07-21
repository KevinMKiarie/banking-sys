from datetime import datetime


class MPesaIntegration:
    """
    Simulates Safaricom M-Pesa integration.
    In production this would call the Safaricom Daraja API.
    """

    # Standard Safaricom send-money tariff bands (amount range -> charge in KES)
    CHARGES = {
        (1,     49):     0,
        (50,    100):    0,
        (101,   500):    7,
        (501,   1000):   13,
        (1001,  1500):   23,
        (1501,  2500):   33,
        (2501,  3500):   53,
        (3501,  5000):   57,
        (5001,  7500):   78,
        (7501,  10000):  90,
        (10001, 15000):  100,
        (15001, 20000):  105,
        (20001, 35000):  108,
        (35001, 50000):  108,
        (50001, 150000): 108,
    }

    def __init__(self):
        self.__paybill_accounts: dict = {}   # paybill_number -> {account, name}
        self.__till_numbers: dict     = {}   # till_number -> business_name
        self.__transactions: list     = []

    def register_paybill(self, paybill_number: str, bank_account: str, business_name: str):
        self.__paybill_accounts[paybill_number] = {
            "account": bank_account,
            "name": business_name
        }
        print(f"[M-Pesa] Paybill {paybill_number} registered for {business_name}")

    def register_till(self, till_number: str, business_name: str):
        self.__till_numbers[till_number] = business_name
        print(f"[M-Pesa] Till {till_number} registered for {business_name}")

    def get_charge(self, amount: float) -> float:
        for (low, high), charge in self.CHARGES.items():
            if low <= amount <= high:
                return float(charge)
        return 0.0

    def send_money(self, sender_phone: str, receiver_phone: str, amount: float) -> dict:
        """Person-to-person M-Pesa transfer."""
        charge    = self.get_charge(amount)
        total     = amount + charge
        timestamp = datetime.now()
        ref       = f"MP{timestamp.strftime('%y%m%d%H%M%S')}"

        result = {
            "reference":      ref,
            "sender":         sender_phone,
            "receiver":       receiver_phone,
            "amount":         amount,
            "charge":         charge,
            "total_deducted": total,
            "timestamp":      timestamp.isoformat(),
            "status":         "SUCCESS",
        }
        self.__transactions.append(result)
        print(
            f"[M-Pesa] {ref}: KES {amount:,.2f} sent "
            f"from {sender_phone} to {receiver_phone}. Charge: KES {charge}"
        )
        return result

    def pay_bill(self, phone: str, paybill: str, account_ref: str, amount: float) -> dict:
        """Pay a business via paybill number."""
        if paybill not in self.__paybill_accounts:
            raise LookupError(f"Paybill {paybill} not registered")

        business  = self.__paybill_accounts[paybill]
        charge    = self.get_charge(amount)
        timestamp = datetime.now()
        ref       = f"PB{timestamp.strftime('%y%m%d%H%M%S')}"

        result = {
            "reference":  ref,
            "phone":      phone,
            "paybill":    paybill,
            "account_ref": account_ref,
            "business":   business["name"],
            "amount":     amount,
            "charge":     charge,
            "timestamp":  timestamp.isoformat(),
            "status":     "SUCCESS",
        }
        self.__transactions.append(result)
        print(
            f"[M-Pesa] {ref}: KES {amount:,.2f} paid to {business['name']} "
            f"(Paybill {paybill}, Acct: {account_ref}). Charge: KES {charge}"
        )
        return result

    def buy_airtime(self, phone: str, amount: float) -> dict:
        """Buy airtime for any Safaricom number."""
        if amount < 5 or amount > 10_000:
            raise ValueError("Airtime amount must be between KES 5 and KES 10,000")
        ref = f"AT{datetime.now().strftime('%y%m%d%H%M%S')}"
        print(f"[M-Pesa] {ref}: KES {amount:,.2f} airtime sent to {phone}")
        return {"reference": ref, "phone": phone, "amount": amount, "status": "SUCCESS"}

    def get_transaction_history(self, phone: str) -> list:
        return [
            t for t in self.__transactions
            if t.get("sender") == phone or t.get("receiver") == phone or t.get("phone") == phone
        ]

    def __repr__(self) -> str:
        return f"MPesaIntegration(paybills={len(self.__paybill_accounts)}, transactions={len(self.__transactions)})"
