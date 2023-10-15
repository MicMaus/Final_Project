# from collections.abc import Iterator
# from error_handl_decorator import error_handling_decorator
from error_handl_decorator import CustomError
from collections import UserDict
import re
import datetime
import pickle

# classes
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value
    
    def __str__(self):
        return self.value

    @property
    def value(self) -> str:
        return self._value


class Name(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if new_value.isalpha():
            self._value = new_value
        else:
            raise CustomError("please provide valid name")


class Phone(Field):
    def __init__(self, value):
        super().__init__(str(value))
    
    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value



class Birthday(Field):
    def __init__(self, value): 
        super().__init__(value)
    
    @Field.value.setter
    def value(self, new_value):
        dob = new_value.date()
        self._value = dob
    

class Email(Field):
    def __init__(self, value):
        super().__init__(str(value))
    
    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value


class Address(Field):
    def __init__(self, value):
        super().__init__(str(value))

    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value


class Note(Field):
    def __init__(self, value):
        super().__init__(str(value))

    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value


class Record:
    def __init__(self, name, phone=None, birthday=None, email=None, address=None, note=None): 
        self.name = Name(value=name)
        self.phones = []
        if phone:
            self.add_new_phone(phone)
        if birthday:
            self.birthday = Birthday(value=birthday)
        if email:
            self.email = Email(value=email)
        if address:
            self.address = Address(value=address)
        if note:
            self.note = Note(value=note)

    def days_to_birthday(self):
        current_date = datetime.date.today()
        next_birthday = datetime.date(current_date.year, self.birthday.value.month, self.birthday.value.day)
        
        if current_date > next_birthday:
            next_birthday = datetime.date(current_date.year + 1, self.birthday.value.month, self.birthday.value.day)
            
        days_until_birthday = (next_birthday - current_date).days

        return days_until_birthday

    def add_new_phone(self, phone): 
        self.phones.append(Phone(value=phone))

    def amend_phone(self, name, new_phone, old_phone): 
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == old_phone:
                self.phones.remove(stored_phone)
                self.add_new_phone(new_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")

    def remove_phone(self, phone):
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == phone:
                self.phones.remove(stored_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")


phone_book_file = r'./phone_book'


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        try:
            with open(phone_book_file, "rb") as fh:
                deserialized_book = pickle.load(fh)
            self.data = deserialized_book
        except:
            pass
    
    def save_changes():
        with open(phone_book_file, "wb") as fh:
                pickle.dump(phone_book, fh)

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n): # n-number of records per page. is defined in show_page function
        contacts_per_page = n
        contacts = list(self.data.keys())
        index = 0

        while index < len(contacts):
            yield contacts[index:index + contacts_per_page]
            index += contacts_per_page

phone_book = AddressBook()