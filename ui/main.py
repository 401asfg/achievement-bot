from command import is_command, interpret_command, exceptions


def on_message(message: str):
    if not is_command(message):
        return

    try:
        interpret_command(message, "user")
    except exceptions.LexError:
        print("Unknown word entered")
    except exceptions.ParsingError:
        print("Command was improperly formatted")


def main():
    print("Enter a command")

    message = ""

    while message != "quit":
        message = input()
        on_message(message)

    print("Goodbye")


main()
