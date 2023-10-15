from command_parser import parse_input
from classes import AddressBook

# tuple of commands to close the bot
close_app = ('exit', 'good bye', 'close') 


def main():
    while True:
        user_input = input("your command (type 'guide' to display list of available commands): ").lower()

        if user_input.startswith(close_app):
            print("Good bye!")
            AddressBook.save_changes()
            break

        result = parse_input(user_input) 
        if result is not None: 
            print(result) 


if __name__ == "__main__":
    main()
