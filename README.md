# Kenyan Banking System

A Python project that simulates how different Kenyan banks process transactions. Built around object-oriented principles — encapsulation, inheritance, and abstraction. The idea was to model real banking behaviour as closely as possible without hitting actual bank APIs.

It covers KCB, Equity Bank, and M-Pesa, and lets you open accounts, deposit, withdraw, transfer between banks, and track transaction history.

---

## What you need

- Python 3.10 or higher
- That's it. No external libraries required.

---

## Getting started

Clone the repo and step into it:

```bash
git clone https://github.com/KevinMKiarie/banking-sys.git
cd banking-sys
```

If you want to keep things clean, set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

---

## Running it

From the root of the project:

```bash
python3 main.py
```

You should see output walking through account creation, deposits, withdrawals, inter-bank transfers via PesaLink, M-Pesa send money, paybill payments, and mini statements for each customer.

---

## Project structure

```
banking-sys/
├── main.py                  # Entry point — run this
├── models/
│   ├── customer.py          # Customer with ID and phone validation
│   ├── account.py           # Account types and balance management
│   └── transaction.py       # Transaction records (immutable once created)
└── banks/
    ├── base_bank.py         # Abstract class all banks must implement
    ├── kcb.py               # KCB Bank — 0.2% transfer fee, 500k daily limit
    ├── equity.py            # Equity Bank — 0.15% transfer fee, 300k daily limit
    ├── mpesa.py             # M-Pesa — send money, paybill, airtime
    └── banking_system.py    # Ties everything together, handles interbank transfers
```

---

## How it works

Each bank inherits from `BaseBank` and must implement its own version of `open_account`, `deposit`, `withdraw`, `transfer`, and `get_balance`. The `BankingSystem` class sits on top and handles anything that crosses bank boundaries, like a PesaLink transfer from KCB to Equity.

Account balances are private and can only be changed through controlled methods, not set directly. Same goes for customer data — you read it through properties, you can't just overwrite it.

M-Pesa runs separately and uses Safaricom's standard tariff bands to calculate charges on each transaction.

---

## Branches

The work was split across two days:

- `feature/models` — core data models (Customer, Account, Transaction)
- `feature/banks` — bank implementations and M-Pesa integration
- `main` — both merged and ready to run
