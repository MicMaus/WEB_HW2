import re

# Define a string containing Ukrainian symbols and their corresponding translations
UKRAINIAN_SYMBOLS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "je",
    "zh",
    "z",
    "y",
    "i",
    "ji",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "ju",
    "ja",
)

# Create a dictionary to store the translation mappings
TRANS = {}

# Populate the dictionary with Unicode code points of Ukrainian symbols as keys and their translations as values
for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    """
    Normalize a string by replacing Ukrainian symbols and non-word characters.

    This function takes a string and replaces Ukrainian symbols with their Latin counterparts,
    as defined in the `TRANS` dictionary. Additionally, it replaces non-word characters with
    underscores to ensure a valid filename.
    :param name: The string to be normalized.
    :return: The normalized string.
    """
    # Split the string into name and extension
    name, *extension = name.split(".")

    # Translate Ukrainian symbols and replace non-word characters with underscores
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)

    return f"{new_name}"
