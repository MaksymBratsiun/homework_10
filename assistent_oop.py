from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, name):
        self.value = name


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Record(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = Name(name)
        self.phones = []
        self.birthday = ''

    def add_phone(self, phone):
        list_phones = []
        for number in self.phones:
            list_phones.append(number.value)
        if phone not in list_phones:
            list_phones.append(phone)
        self.phones.clear()
        for number in list_phones:
            self.phones.append(Phone(number))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            birthday = datetime(year=datetime.now().year,
                                month=int(self.birthday[0:2]),
                                day=int(self.birthday[3:5]))
            if today > birthday:
                birthday = datetime(year=datetime.now().year + 1,
                                    month=int(self.birthday[0:2]),
                                    day=int(self.birthday[3:5]))
            return f"{(birthday - today + timedelta(days=1)).days} days to {self.name.value}'s birthday"
        else:
            return f"{self.name.value.title()}'s date of birth  not set"

    def get_info(self):
        phones_info = ""
        birthday_str = ""
        for phone in self.phones:
            phones_info += f"{phone.value}, "
        if self.birthday:
            birthday_str = f"(Birthday at month {self.birthday.value[0:2]}, day {self.birthday.value[3:5]})"
        return f"{self.name.value.title()}{birthday_str}: {phones_info[:-2]}"

    def delete_phone(self, delete_phone):
        old_len = len(self.phones)
        for phone in self.phones:
            if phone.value == delete_phone:
                self.phones.pop(self.phones.index(phone))
        if len(self.phones) == old_len:
            return False
        else:
            return True

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.delete_phone(old_phone)
                self.add_phone(new_phone)


class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            new_record = Record(record.name.value)
            exists_record = book.get_record(record.name.value)
            for phone in exists_record.phones:
                new_record.add_phone(phone.value)
            for phone in record.phones:
                new_record.add_phone(phone.value)
            if record.birthday:
                new_record.add_birthday(record.birthday.value)
            elif exists_record.birthday.value:
                new_record.add_birthday(exists_record.birthday.value)

            self.data[record.name.value] = new_record

    def get_all_record(self):
        return self.data

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def has_record(self, name):
        return bool(self.data.get(name))

    def find_record(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

    def delete_record(self, name):
        del self.data[name]


book = AddressBook()


def input_error(func):  # decorator @input_error
    def inner_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as e:
            result = f"Name {e} not found."
        except IndexError:
            result = "Phone number not entered."
        except TypeError:
            result = "Phone number not entered."
        finally:
            return result

    return inner_function


@input_error
def add_handler(user_input):
    if len(user_input) >= 2:
        record = Record(user_input[0])
        record.add_phone(user_input[1])
        book.add_record(record)
    return f"{str(user_input[0]).title()}: {user_input[1]} successfully added"


def birthday_handler(user_input):
    if len(user_input) >= 3:
        if book.get_record(user_input[0]):
            record = book.get_record(user_input[0])
            date_str = f"{user_input[1]} {user_input[2]}"
            record.add_birthday(date_str)
            book.add_record(record)
            return f"{str(user_input[0]).title()}'s Birthday set at month {user_input[1]}, day {user_input[2]}"
        else:
            return f"Incorrect input. Enter 'Name Month(MM) Day(dd)'"
    else:
        return f"Name not found"


def left_handler(user_input):
    pass


@input_error
def change_handler(user_input):
    if len(user_input) >= 2:
        if user_input[0] == user_input[1]:
            return f"Its the same phone {user_input[1]}"
        elif book.find_record(user_input[0]):
                found_record = book.find_record(user_input[0])
                found_record.change_phone(user_input[0], user_input[1])
                book.delete_record(found_record.name.value)
                book.add_record(found_record)
                return f"Contact {found_record.name.value.title()}: old number {user_input[0]} " \
                       f"successfully changed to {user_input[1]}"
        else:
            return f"Phone {user_input[0]} no found"


@input_error
def delete_handler(user_input):
    if user_input[0]:
        book.delete_record(user_input[0])
        return f"Contact {user_input[0].title()} deleted"


def exit_handler(user_input):
    return "Good bye!"


def error_handler(user_input):
    return 'Command not found. Enter "help" for view command list.'


def hello_handler(user_input):
    return 'How can I help you?'


def help_handler(user_input):
    text = """ 
    "add" - add name(one word) and phone(digit): "add Ivan +380931234567"
    "close", "exit", "good bye" - exit from application: "exit"
    "change" - change old phone if exists to new phone: "change +380931234567 +380937654321"
    "delete", "remove" - delete contact: "delete Ivan"
    "hello" -  print How can I help you?: "hello"
    "help": print help list: "help"
    "search", "phone" - print phone or name: "search Ivan" or "search +380501234567"
    "show all" - print names and phones: "show all" """
    return text


def input_parser():
    input_list = []
    user_input = str(input("Enter: ")).lower()
    if not user_input.find(".") == -1:
        exit()
    else:
        user_input = user_input.strip()
        input_list = user_input.split(" ")

        if len(input_list) >= 2:

            if input_list[0] == "good" and input_list[1] == "bye":
                input_list[0] = input_list[0] + " " + input_list.pop(1)

            if input_list[0] == "show" and input_list[1] == "all":
                input_list[0] = input_list[0] + " " + input_list.pop(1)

        return input_list


@input_error
def search_handler(user_input):
    if len(user_input):
        if book.find_record(user_input[0]):
            return book.find_record(user_input[0]).get_info()
        else:
            return f"{user_input[0]} not found"


def show_handler(user_input):
    phone_book_list = []
    for key, rec in book.get_all_record().items():
        phone_book_list.append(rec.get_info())
    return "\n".join(phone_book_list)


HANDLER_DICT = {
    "add": add_handler,
    "close": exit_handler,
    "change": change_handler,
    "exit": exit_handler,
    "good bye": exit_handler,
    "hello": hello_handler,
    "help": help_handler,
    "phone": search_handler,
    "remove": delete_handler,
    "search": search_handler,
    "show all": show_handler,
    "delete": delete_handler
}


def get_handler(operator):
    return HANDLER_DICT.get(operator, error_handler)


def main():
    # while True:
    #     user_input = input_parser()
    #     string = str(get_handler(user_input[0])(user_input[1:]))
    #     print(string)
    #     if string == "Good bye!":
    #         exit()
    rec = Record('ivan')
    rec.add_phone('123')
    rec.add_birthday('01 01')
    book.add_record(rec)
    rec1 = Record('petro')
    rec1.add_phone('321')
    rec1.add_birthday('01 02')
    book.add_record(rec1)
    phone_book_list = []
    for key, rec in book.get_all_record().items():
        phone_book_list.append(rec.get_info())
    print("\n".join(phone_book_list))


if __name__ == '__main__':
    main()
