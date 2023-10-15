from functions import *
from error_handl_decorator import error_handling_decorator

# commands parser, which calls the functions providing needed arguments
@error_handling_decorator
def parse_input(user_input):
    user_input = check_command(user_input, commands)
    for request in commands:  # dict with commands
        if user_input.startswith(request):
            func = commands[request]

            if func == add_contact:
                name = input('please provide a contact name: ')
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
                info_to_amend = input('what type of information will be amended (phone / birthday / email / address / note): ')
                
                if info_to_amend == 'phone':
                    new_phone_number = phone_input()
                    old_phone_number = input('please provide the phone number to be replaced: ') 
                    return change_phone(name, new_phone_number, old_phone_number)
                
                elif info_to_amend == 'birthday':
                    birth_date = dob_input()
                    return add_contact(name, birthday=birth_date)
                
                elif info_to_amend == 'email':
                    email == email_input()
                    return add_contact(name, email=email)

                elif info_to_amend == 'address':
                    address = input('please provide the new address: ')
                    return add_contact(name, address=address)

                elif info_to_amend == 'note':
                    note = input('please provide the new note: ')
                    return add_contact(name, note=note)           
                    
                elif info_to_delete != 'phone' and info_to_delete != 'birthday' and info_to_delete != 'email' and info_to_delete != 'address' and info_to_delete != 'note':
                    raise CustomError ("please provide valid field to amend")
                
            

            elif func == show_page:
                page = input('please provide the page to display: ')
                return func(page)
            
            elif func == remove_contact:
                name = name_input()
                return func(name)

            elif func == remove_info: 
                name = name_input()
                info_to_delete = input('what type of information will be deleted (phone / birthday / email / address / note): ')
                if info_to_delete == 'phone':
                    phone_number = phone_input()
                    return func(name, info_to_delete, phone_number)
                
                elif info_to_delete != 'phone' and info_to_delete != 'birthday' and info_to_delete != 'email' and info_to_delete != 'address' and info_to_delete != 'note':
                    raise CustomError ('please provide valid field to be deleted')
                
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
            
            
            elif func == add_note:
                print('please write your note here (duble enter to finish): ')
                text = []
                while True:
                    new_text = input()
                    if not new_text:
                        break
                    text.append(new_text)
                tags = input('please provide tegs separeted with spaces: ')
                return func('\n'.join(text), tags)

            elif func == delete_note:
                id = input('please provide a note id: ')
                return func(id)

            elif func == edit_text:
                id = input('please provide a note id: ')
                print('please write your note here (duble enter to finish): ')
                text = []
                while True:
                    new_text = input()
                    if not new_text:
                        break
                    text.append(new_text)
                return func(id, '\n'.join(text))

            elif func == delete_tag:
                id = input('please provide a note id: ')
                tag = input('what tag do you want to delete:')
                return func(id, tag)

            elif func == add_tags:
                id = input('please provide a note id: ')
                tags = input('please provide tegs separeted with spaces: ')
                return func(id, tags)


            else:  #run func which don't need args. eg.hello, help, show all
                return func()

    raise CustomError("please provide a valid command")
