from abstract_classes import *
from command_parser import parse_input, bot_config


def main():
    if not bot_config():
        print("There is no configuration file. Can not work without it! Good bye!")
        return

    while True:
        user_input = input(
            "your command (type 'guide' to display list of available commands): "
        ).lower()

        result = parse_input(user_input)

        if result is not None and isinstance(result, MainStyleClass):
            result.display_style()

        if user_input == "exit" or user_input == "close":
            break


if __name__ == "__main__":
    main()
