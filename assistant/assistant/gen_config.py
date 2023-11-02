from pathlib import Path


def gen_config_file():
    config_file = "bot_config.txt"
    if Path(config_file).exists():
        return config_file

    config = {
        "contacts_per_page": "2",
        "notebook_file": "notes.bin",
        "addressbook_file": "phone_book.bin",
        "account_sid": "ACb5c2ef81d62b89df899d7eb7a74be13d",
        "auth_token": "c72560502a1d65f1173a7a0bb7e13389",
        "account_phone": "+16173796725",
        "help_file": "help.txt",
    }
    with open(config_file, "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

    return config_file


CONFIG_FILE = gen_config_file()
