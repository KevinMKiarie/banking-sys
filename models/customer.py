import re
from datetime import date


class Customer:
    def __init__(self, national_id: str, full_name: str, phone: str, email: str = None):
        self.__national_id = self.__validate_id(national_id)
        self.__full_name = full_name.strip().title()
        self.__phone = self.__validate_phone(phone)
        self.__email = email
        self.__date_registered = date.today()

    def __validate_id(self, id_number: str) -> str:
        id_number = id_number.strip()
        if not re.match(r"^\d{7,8}$", id_number):
            raise ValueError(f"Invalid Kenyan National ID: {id_number}")
        return id_number

    def __validate_phone(self, phone: str) -> str:
        phone = phone.strip().replace(" ", "")
        if phone.startswith("07") or phone.startswith("01"):
            phone = "+254" + phone[1:]
        if not re.match(r"^\+2547\d{8}$|^\+2541\d{8}$", phone):
            raise ValueError(f"Invalid Kenyan phone number: {phone}")
        return phone

    @property
    def national_id(self) -> str:
        return self.__national_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if value and "@" not in value:
            raise ValueError("Invalid email address")
        self.__email = value

    @property
    def date_registered(self) -> date:
        return self.__date_registered

    def __repr__(self) -> str:
        return f"Customer(id={self.__national_id}, name={self.__full_name}, phone={self.__phone})"
