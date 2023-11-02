import datetime
import os
import re

from classes import phone_book
from country_codes import country_codes


def name_input_for_add():
    def name_validation(name):
        if not name:
            return False
        else:
            return True

    while True:
        input_name = input("Please provide a contact name: ")
        check = name_validation(input_name)
        if check:
            return input_name
        else:
            print("Name is mandatory field. Try again")


def name_input():
    def name_validation(name):
        if name not in phone_book:
            return False
        else:
            return True

    while True:
        input_name = input("Please provide a contact name: ")
        check = name_validation(input_name)
        if check:
            return input_name
        else:
            print("Please provide a valid name. Try again")


def dob_input():
    def birthday_format_check(birth_date):
        if not birth_date:
            return birth_date

        else:
            if not re.match(r"\d{4}-\d{2}-\d{2}", birth_date):
                return False

            # convert to datetime format
            try:
                date_value = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
            except:
                return False

            # check the date correctness
            if not (
                1900 <= date_value.year <= datetime.date.today().year
                and 1 <= date_value.month <= 12
                and 1 <= date_value.day <= 31
            ):
                return False

            return date_value

    while True:
        input_birth_date = input("Please provide a bithday in a format YYYY-MM-DD: ")
        dob = birthday_format_check(input_birth_date)
        if dob != False:
            return dob

        else:
            print("Please enter a valid birthdate in the format YYYY-MM-DD. Try again")


def email_input():
    def email_format_check(email):
        if not email:
            return True

        elif not re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        ):
            return False

        return True

    while True:
        input_email = input("Please provide an email: ")
        check = email_format_check(input_email)

        if check:
            return input_email

        else:
            print("Please provide an email in the correct format. Try again")


def phone_input():
    def phone_format_check(phone_number):
        if not phone_number:
            return True

        if re.match(r"^\+\d+$", phone_number):
            phone_digits = re.sub(r"[^\d]", "", phone_number)
            found_country = None
            for country, code in country_codes.items():
                if phone_digits.startswith(str(code)):
                    found_country = country
                    print(f"Phone number of: {found_country}")
                    return True
            if not found_country:
                print("Country code unknown. Please try again.")
                return False
        else:
            print(
                "Invalid phone format. The number must start with + and contain digits only. Please try again."
            )
            return False

    while True:
        input_phone = input("Please provide a new phone: ")
        check = phone_format_check(input_phone)
        if check:
            return input_phone


def path_input():
    def path_check(path):
        if not os.path.exists(path):
            return False
        else:
            return True

    while True:
        input_path = input(
            "Enter the path to the folder containing unorganized files: "
        )
        check = path_check(input_path)
        if check:
            return input_path
        else:
            print("Provided path is not valid. Try again")


def phone_index_input(contact):
    enumerated_phones = enumerate(contact.phones)
    for index, phone_num in enumerated_phones:
        phone_number = phone_num.value
        print(f"{index} is index of phone number {phone_number}")

    while True:
        index_input = int(input("Please enter a phone index: "))
        try:
            phone = contact.phones[index_input]
            return phone
        except IndexError:
            print("Phone index not found. Try again")
