from Final_Project.error_handl_decorator import CustomError
from Final_Project.classes import *
from Final_Project.input_format_verification import *
import difflib  # matches library
from Final_Project.notebook import *
from pathlib import Path
import Final_Project.main_sorting_files
from twilio.rest import Client
from Final_Project.user_config import Config
from Final_Project.gen_config import *
import time
from colorama import Fore, Style


# commands parser, which calls the functions providing needed arguments
@error_handling_decorator
def parse_input(user_input):
    user_input = check_command(user_input, commands)
    for request in commands:  # dict with commands
        if user_input.startswith(request):
            func = commands[request]

            if func == add_contact:
                name = name_input_for_add()
                new_phone_number = phone_input()
                birth_date = dob_input()
                email = email_input()
                address = input('please provide an address: ')
                note = input('please provide a note: ')
                return func(name, new_phone_number, birth_date, email, address, note)

            elif func == show_contact:
                name = input('please provide a contact name: ')
                return func(name)

            elif func == change_info:
                name = name_input()
                info_to_amend = input(
                    'what type of information will be amended (phone / birthday / email / address / note): ')
                contact = phone_book.get(name)

                if info_to_amend == 'phone':
                    print("Please choose index of the phone to be amended:")
                    old_phone_number = str(phone_index_input(contact))
                    new_phone_number = phone_input()
                    return change_phone(name, new_phone_number, old_phone_number)

                elif info_to_amend == 'birthday':
                    birth_date = dob_input()
                    return add_contact(name, birthday=birth_date)

                elif info_to_amend == 'email':
                    email = email_input()
                    return add_contact(name, email=email)

                elif info_to_amend == 'address':
                    address = input('please provide the new address: ')
                    return add_contact(name, address=address)

                elif info_to_amend == 'note':
                    note = input('please provide the new note: ')
                    return add_contact(name, note=note)

                elif (info_to_amend != 'phone' and info_to_amend != 'birthday'
                      and info_to_amend != 'email' and info_to_amend != 'address' and info_to_amend != 'note'):
                    raise CustomError("please provide valid field to amend")

            elif func == show_page:
                page = input('please provide the page to display: ')
                return func(page)

            elif func == remove_contact:
                name = name_input()
                return func(name)

            elif func == remove_info:
                name = name_input()
                contact = phone_book.get(name)
                info_to_delete = input('what type of information will be deleted (phone / birthday / email / address '
                                       '/ note): ')
                if info_to_delete == 'phone':
                    print("Please choose index of the phone to be removed:")
                    phone_number = str(phone_index_input(contact))
                    return func(name, info_to_delete, phone_number)

                elif (info_to_delete != 'phone' and info_to_delete != 'birthday'
                      and info_to_delete != 'email' and info_to_delete != 'address' and info_to_delete != 'note'):
                    raise CustomError('please provide valid field to be deleted')

                return func(name, info_to_delete)

            elif func == search:
                search_word = input('please provide a search request: ')
                return func(search_word)

            elif func == dtb:
                name = name_input()
                return func(name)

            elif func == show_birthdays_soon:
                while True:
                    try:
                        days = int(input('Enter the number of days: '))
                        break  # Вихід із циклу, якщо користувач ввів число правильно
                    except ValueError:
                        print("Please enter a valid number.")

                return func(days)


            # Notes commands
            elif func == add_note:
                text = input_note_params("text")
                tags = input_note_params("tags")
                return func(text, tags)

            elif func == delete_note:
                id = input_note_params("id")
                return func(id)

            elif func == edit_text:
                id = input_note_params("id")
                text = input_note_params("text")
                return func(id, text)

            elif func == delete_tag:
                id = input_note_params("id")
                tag = input_note_params("tag")
                return func(id, tag)

            elif func == add_tags:
                id = input_note_params("id")
                tags = input_note_params("tags")
                return func(id, tags)

            elif func == find_by_tag:
                tags = input_note_params("tags")
                show_desc = input_note_params("show_desc")
                return func(tags, show_desc)
            # end notes commands

            elif func == sort_files:
                folder_path = path_input()
                return func(folder_path)

            elif func == send_sms:
                contact_name = input("Enter the name of the contact to send SMS: ")
                contact = phone_book.get(contact_name)
                if contact:
                    if len(contact.phones) > 1:
                        print("Choose a phone number to send the SMS:")
                        for i, phone in enumerate(contact.phones, start=1):
                            print(f"{i}. {phone}")

                        try:
                            choice = int(input("Enter the number of the phone to send SMS: "))
                            if 1 <= choice <= len(contact.phones):
                                phone = contact.phones[choice - 1]
                            else:
                                print("Invalid choice. SMS not sent.")
                                continue
                        except ValueError:
                            print("Invalid input. SMS not sent.")
                            continue
                    else:
                        phone = contact.phones[0]

                    message = input("Enter the SMS message: ")
                    try:
                        send_sms(phone, message)
                        for _ in range(3):
                            print("Sending", end="", flush=True)
                            time.sleep(0.25)
                            for i in range(3):
                                print(".", end="", flush=True)
                                time.sleep(0.25)
                            print("\r", end="", flush=True)
                        print(Fore.BLUE + "Message sent." + Style.RESET_ALL)
                    except Exception as e:
                        print(f"Failed to send SMS to {phone}: {str(e)}")
                else:
                    print("Contact not found")

            elif func == call:
                contact_name = input("Enter the name of the contact to make a call: ")
                contact = phone_book.get(contact_name)
                if contact:
                    if len(contact.phones) > 1:
                        print("Choose a phone number to make the call:")
                        for i, phone in enumerate(contact.phones, start=1):
                            print(f"{i}. {phone}")

                        try:
                            choice = int(input("Enter the number of the phone to make the call: "))
                            if 1 <= choice <= len(contact.phones):
                                phone = contact.phones[choice - 1]
                            else:
                                print("Invalid choice. Call not made.")
                                continue
                        except ValueError:
                            print("Invalid input. Call not made.")
                            continue
                    else:
                        phone = contact.phones[0]

                    message = input("Enter the call message: ")

                    try:
                        call(phone, message)
                        for _ in range(6):
                            print(f"Calling {phone}", end="", flush=True)
                            time.sleep(0.25)
                            for i in range(3):
                                print(".", end="", flush=True)
                                time.sleep(0.25)
                            print("\r", end="", flush=True)
                        print(Fore.BLUE + "Call in progress." + Style.RESET_ALL)
                    except Exception as e:
                        print(f"Failed to make a call to {phone}: {str(e)}")
                else:
                    print("Contact not found")

            else:  # run func which don't need args. e.g.hello, help, show all
                return func()

    raise CustomError("please provide a valid command")
