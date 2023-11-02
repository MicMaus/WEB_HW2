import difflib  # matches library

from twilio.rest import Client

import main_sorting_files
from classes import *
from gen_config import *
from input_format_verification import *
from notebook import *
from user_config import Config
from error_handl_decorator import *

config = Config(CONFIG_FILE)
notes = NoteBook()


def view_notes():
    message = ""
    for note in notes.values():
        message += "\n" + str(note) + "\n"
    if not message:
        message = "You have no notes yet"
    return message


def add_note():
    text = input_note_params("text")
    tags = input_note_params("tags")

    tag_list = str_to_tags(tags)
    note = Note(text, tag_list)
    notes.add_note(note)
    return "Note was successfully added"


def delete_note():
    id = input_note_params("id")
    notes.delete_note(id)
    return "Note was successfully removed"


def edit_text() -> str:
    id = input_note_params("id")
    new_text = input_note_params("text")

    note = notes.find_id(id)
    note.edit_text(new_text)
    notes.save()
    return "Note was successfully edited"


def add_tags() -> str:
    id = input_note_params("id")
    tags = input_note_params("tags")

    tag_list = str_to_tags(tags)
    note = notes.find_id(id)
    note.add_tags(tag_list)
    notes.save()
    return f"Tags were successfully added to the note with id {id}"


def delete_tag() -> str:
    id = input_note_params("id")
    tag = input_note_params("tag")

    note = notes.find_id(id)
    note.remowe_tag(tag)
    notes.save()
    return "Tags were successfully deleted"


def find_by_tag() -> str:
    tags = input_note_params("tags")
    show_desc = input_note_params("show_desc")

    intersec = " and " in tags
    tags = tags.replace(" and ", " ").replace(" or ", " ")
    tag_list = []
    tag_list.extend(tags.split(" "))
    for i in range(len(tag_list)):
        if not tag_list[i].startswith("#"):
            tag_list[i] = "#" + tag_list[i]

    result = notes.find_by_tag(tag_list, intersec, show_desc)

    message = ""
    for note in result:
        message += "\n" + str(note) + "\n"
    if not message:
        message = "Nothing found. Correct search conditions."
    return message


def input_note_params(param: str):
    correct = False
    value = ""
    while not correct:
        if param == "id":
            value = input("Please provide a note id: ")
            correct = value in notes

        elif param == "text":
            print("Please write your note here (double enter to finish): ")
            value = []
            while True:
                new_text = input()
                if not new_text:
                    break
                value.append(new_text)
            value = "\n".join(value)
            correct = value != ""

        elif param == "tag":
            value = input("Please provide a tag: ")
            correct = value in notes.tag_cloud

        elif param == "tags":
            value = input("Please provide tags separated with spaces: ")
            correct = value != ""

        elif param == "show_desc":
            value = input("Show newest on the top (Y/N)? ")
            value = value.lower() == "y"
            correct = True

        if not correct:
            print("Incorrect data. Try again")

    return value


def str_to_tags(text: str):
    tags = []
    for tag in text.split(" "):
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = "#" + tag
        tags.append(tag)
    return tags


# parameter cutoff regulates sensitivity for matching, 1.0 - full match, 0.0 - input always matches
def find_closest_match(user_input, commands):
    closest_match = difflib.get_close_matches(user_input, commands, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        return None


def check_command(user_input, commands):
    if user_input in commands:
        return user_input

    closest_match = find_closest_match(user_input, commands)
    if closest_match:
        print(closest_match)
        return closest_match
    else:
        return user_input


# adding new contact/phone number
@error_handling_decorator
def add_contact():
    name = name_input_for_add()
    if name in phone_book:
        return "This name already exist"
    phone = phone_input()
    birthday = dob_input()
    email = email_input()
    address = input("please provide an address: ")
    note = input("please provide a note: ")

    record = Record(name, phone, birthday, email, address, note)
    phone_book.add_record(record)
    return "New contact successfully added"


@error_handling_decorator
def change_contact_field(
    name, phone=None, birthday=None, email=None, address=None, note=None
):
    record = phone_book[name]

    if phone:
        record.add_new_phone(phone)
    elif birthday:
        record.birthday = Birthday(value=birthday)
    elif email:
        record.email = Email(value=email)
    elif address:
        record.address = Address(value=address)
    elif note:
        record.note = Note(value=note)

    return "New information successfully added to the existing contact"


@error_handling_decorator
def change_info():
    name = name_input()
    info_to_amend = input(
        "what type of information will be amended (phone / birthday / email / address / note): "
    )
    contact = phone_book.get(name)

    if info_to_amend == "phone":
        print("Please choose index of the phone to be amended:")
        old_phone_number = str(phone_index_input(contact))
        new_phone_number = phone_input()
        return change_phone(name, new_phone_number, old_phone_number)

    elif info_to_amend == "birthday":
        birthday = dob_input()
        return change_contact_field(name, birthday=birthday)

    elif info_to_amend == "email":
        email = email_input()
        return change_contact_field(name, email=email)

    elif info_to_amend == "address":
        address = input("please provide the new address: ")
        return change_contact_field(name, address=address)

    elif info_to_amend == "note":
        note = input("please provide the new note: ")
        return change_contact_field(name, note=note)

    elif (
        info_to_amend != "phone"
        and info_to_amend != "birthday"
        and info_to_amend != "email"
        and info_to_amend != "address"
        and info_to_amend != "note"
    ):
        raise CustomError("please provide valid field to amend")


# change the phone number
@error_handling_decorator
def change_phone(name, new_phone, old_phone):
    if not new_phone or not old_phone:
        raise CustomError(
            "Please provide a name, a new number and an old number separated by a space"
        )

    record = phone_book[name]
    record.amend_phone(name, new_phone, old_phone)
    return "Contact successfully changed"


def remove_contact():
    name = name_input()
    del phone_book[name]
    return "Contact successfully removed"


@error_handling_decorator
def remove_info():
    name = name_input()
    contact = phone_book.get(name)
    field_to_remove = input(
        "what type of information will be deleted (phone / birthday / email / address / note): "
    )
    record = phone_book[name]
    if field_to_remove == "phone":
        print("Please choose index of the phone to be removed:")
        phone = str(phone_index_input(contact))
        record.remove_phone(phone)
        return "Phone number successfully removed"

    elif field_to_remove == "birthday":
        if hasattr(record, "birthday"):
            del record.birthday
            return "Birthday successfully removed"
        else:
            raise CustomError("No birthday exist for this contact")

    elif field_to_remove == "email":
        if hasattr(record, "email"):
            del record.email
            return "Email successfully removed"
        else:
            raise CustomError("No email exist for this contact")

    elif field_to_remove == "address":
        if hasattr(record, "address"):
            del record.address
            return "Address successfully removed"
        else:
            raise CustomError("No address exist for this contact")

    elif field_to_remove == "note":
        if hasattr(record, "note"):
            del record.note
            return "Note successfully removed"
        else:
            raise CustomError("No note exist for this contact")


# show contact details of user
def show_contact(name=None):
    if not name:
        name = name_input()
    record = phone_book[name]
    phone_numbers = []

    for item in record.phones:
        phone_numbers.append(item.value)

    if len(phone_numbers) > 0:
        phone_str = f"{', '.join(phone_numbers)}"
    else:
        phone_str = "No phone numbers"

    if hasattr(record, "birthday"):
        birthday_str = record.birthday.value.strftime("%Y-%m-%d")
    else:
        birthday_str = "No birthday recorded"

    if hasattr(record, "email"):
        email_str = record.email.value
    else:
        email_str = "No email recorded"

    if hasattr(record, "address"):
        address_str = record.address.value
    else:
        address_str = "No address recorded"

    if hasattr(record, "note"):
        note_str = record.note.value
    else:
        note_str = "No note recorded"

    return (
        f"{name}: {phone_str}, {birthday_str}, {email_str}, {address_str}, {note_str}"
    )


# show all contacts info
@error_handling_decorator
def show_all():
    contacts = []
    for record in phone_book:
        one_contact = show_contact(record)
        contacts.append(one_contact)
    if contacts:
        return ";\n".join(contacts)
    else:
        raise CustomError("Phone book is empty")


@error_handling_decorator
def show_page():
    page = input("please provide the page to display: ")
    try:
        page_number = int(page)
        contacts_per_page = int(config["contacts_per_page"])

        if page_number < 1:
            raise CustomError("Pages start from 1")

        contact_batches = list(phone_book.iterator(contacts_per_page))

        if page_number <= len(contact_batches):
            contacts = contact_batches[page_number - 1]
            return ";\n".join([show_contact(contact) for contact in contacts])
        else:
            raise CustomError("Page not found")

    except ValueError:
        raise CustomError("Invalid page number")


def hello():
    return "How can I help you? Please type your command"


@error_handling_decorator
def search():
    search_word = input("please provide a search request: ")
    result = []
    for name, record in phone_book.items():
        if len(record.phones) > 0:
            phone_numbers = ", ".join(phone.value for phone in record.phones)
        else:
            phone_numbers = "No phone numbers recorded"
        try:
            birthday_str = record.birthday.value.strftime("%Y-%m-%d")
        except AttributeError:
            birthday_str = "No birthday recorded"

        try:
            note_str = record.note.value
        except AttributeError:
            note_str = "No note recorded"

        if (
            (search_word in name)
            or (search_word in phone_numbers)
            or (search_word in birthday_str)
            or (search_word in note_str)
        ):
            result.append(show_contact(name))

    if result:
        return ";\n".join(result)
    else:
        raise CustomError("Nothing found")


@error_handling_decorator
def dtb():
    name = name_input()
    record = phone_book[name]
    if not hasattr(record, "birthday"):
        raise CustomError("No birthday recorded")
    return record.days_to_birthday()


# shows upcoming birthdays
@error_handling_decorator
def show_birthdays_soon():
    result = []

    while True:
        try:
            days = int(input("Enter the number of days: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    for name, record in phone_book.items():
        days_until_birthday = record.days_to_birthday()

        if days_until_birthday is not None and days_until_birthday == days:
            result.append(show_contact(name))

    if result:
        return ";\n".join(result)
    else:
        raise CustomError("There are no birthdays for the specified number of days")


@error_handling_decorator
def guide():
    try:
        with open(config["help_file"], "r") as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        raise CustomError("File not found")


def sort_files():
    folder_path = path_input()
    main_sorting_files.main(Path(folder_path))


@error_handling_decorator
def send_sms():
    if "account_sid" not in config or "auth_token" not in config:
        return "There option are not configured"

    account_sid = config["account_sid"]
    auth_token = config["auth_token"]

    client = Client(account_sid, auth_token)

    contact_name = name_input()
    contact = phone_book.get(contact_name)
    if contact:
        message = input("Enter the SMS message: ")
        phone = phone_index_input(contact)
        print(f"Sending sms to the number {phone}")
        # result = GeneralStyle(func, phone, message)
        # # print(result)
        # # return None
    else:
        return "Contact not found"

    try:
        message = client.messages.create(
            from_=config["account_phone"], body=message, to=phone
        )
        message = f"Message was successfully sended on number {phone}!"
    except Exception as e:
        raise CustomError(f"{e.args[2]}. Check your calling settings.")
    return message


@error_handling_decorator
def call():
    if "account_sid" not in config or "auth_token" not in config:
        return "There option are not configured"

    account_sid = config["account_sid"]
    auth_token = config["auth_token"]
    client = Client(account_sid, auth_token)

    contact_name = name_input()
    contact = phone_book.get(contact_name)
    if contact:
        message = input("Enter the message: ")
        phone = phone_index_input(contact)
        print(f"Calling to the number {phone}")
        # result = GeneralStyle(func, phone, message)
        # print(result)
        # return None
    else:
        return "Contact not found"  # or raise CustomError ?

    try:
        message = client.calls.create(
            twiml=f"<Response><Say>{message}</Say></Response>",
            to=phone,
            from_=config["account_phone"],
            machine_detection="DetectMessageEnd",
            machine_detection_timeout=0,
        )
        message = f"Call on number {phone} was successfully doned!"
    except Exception as e:
        raise CustomError(f"{e.args[2]}. Check your calling settings.")

    return message


def bot_config():
    if not config.data:
        return False
    if not "contacts_per_page" in config or not config["contacts_per_page"].isdecimal():
        config["contacts_per_page"] = input_config("contacts_per_page")

    if not "user_folder" in config or not create_folder(config["user_folder"]):
        config["user_folder"] = input_config("user_folder")

    notes.file_name = Path(config["user_folder"], config["notebook_file"])
    phone_book.file_name = Path(config["user_folder"], config["addressbook_file"])

    config.save_config()
    return True


def input_config(param: str):
    correct = False
    value = ""
    while not correct:
        if param == "user_folder":
            value = input("Please enter path to folder where all data will be stored: ")
            correct = create_folder(value)
            response = "Path does not exist!"
        if param == "contacts_per_page":
            value = input(
                "Please enter how many contacts per page do you want to see: "
            )
            correct = value.isdecimal()
            response = "It should be a positive decimal value"
        if not correct:
            print(response)

    return value


def create_folder(user_string: str) -> bool:
    path = Path(user_string)
    try:
        path.mkdir(exist_ok=True)
        return True
    except:
        return False


def close_bot():
    phone_book.save_changes()
    return "Good bye!"
