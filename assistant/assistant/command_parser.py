from abstract_classes import *
from functions import *
from error_handl_decorator import *

# commands parser, which calls the functions

commands = {
    # Contact Style functions
    "add": ContactStyle(add_contact),
    "contact": ContactStyle(show_contact),
    "change field": ContactStyle(change_info),
    "show all": ContactStyle(show_all),
    "page": ContactStyle(show_page),
    "remove field": ContactStyle(remove_info),
    "remove contact": ContactStyle(remove_contact),
    "search": ContactStyle(search),
    "dtb": ContactStyle(dtb),
    "sbs": ContactStyle(show_birthdays_soon),
    # Notes Style functions
    "view notes": NotesStyle(view_notes),
    "new note": NotesStyle(add_note),
    "delete note": NotesStyle(delete_note),
    "edit text": NotesStyle(edit_text),
    "delete tag": NotesStyle(delete_tag),
    "new tags": NotesStyle(add_tags),
    "find tags": NotesStyle(find_by_tag),
    # General Style functions
    "sms": GeneralStyle(send_sms),
    "call": GeneralStyle(call),
    "sort files": GeneralStyle(sort_files),
    "config": GeneralStyle(bot_config),
    "hello": GeneralStyle(hello),
    "guide": GeneralStyle(guide),
    "close": GeneralStyle(close_bot),
    "exit": GeneralStyle(close_bot),
}


@error_handling_decorator
def parse_input(user_input):
    user_input = check_command(user_input, commands)
    for request in commands:  # dict with commands
        if user_input.startswith(request):
            func = commands[request]
            return func

    raise CustomError("please provide a valid command")
