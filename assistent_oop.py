from collections import UserDict


class Field:
    def __init__(self, name):
        Field.value = name


class Name(Field):
    def __init__(self, name):
        Field.value = name


class Phone(Field):
    def __init__(self, value):
        self.value = value


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        list_phones = []
        for number in self.phones:
            list_phones.append(number.value)
        if phone not in list_phones:
            list_phones.append(phone)
        self.phones.clear()
        for number in list_phones:
            self.phones.append(Phone(number))

    def get_info(self):
        phones_info = ''
        for phone in self.phones:
            phones_info += f'{phone.value}, '
        return f'{self.name.value.title()}: {phones_info[:-2]}'

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
                self.phones.append(Phone(new_phone))
                self.phones.pop(self.phones.index(phone))


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


@input_error
def change_handler(user_input):
    if len(user_input) >= 2:
        if user_input[0] == user_input[1]:
            return f"Its the same phone {user_input[1]}"
        elif book.find_record(user_input[0]):
                find_record = book.find_record(user_input[0])
                find_record.change_phone(user_input[0], user_input[1])
                book.delete_record(find_record.name.value)
                book.add_record(find_record)
                return f"Contact {find_record.name.value.title()}: old number {user_input[0]} " \
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


def help_hendler(user_input):
    text = """ 
    "add" - add name(one word) and phone(digit): "add Ivan +380931234567"
    "close", "exit", "good bye" - exit from application: "exit"
    "change" - change old phone if exists to new phone: "change +380931234567 +380937654321"
    "delete" - delete contact: "delete Ivan"
    "hello" -  print How can I help you?: "hello"
    "help": print help list: "help"
    "search" - print phone or name: "search Ivan" or "search +380501234567"
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


HENDLER_DICT = {
    "add": add_handler,
    "close": exit_handler,
    "change": change_handler,
    "exit": exit_handler,
    "good bye": exit_handler,
    "hello": hello_handler,
    "help": help_hendler,
    "search": search_handler,
    "show all": show_handler,
    "delete": delete_handler
}


def get_handler(operator):
    return HENDLER_DICT.get(operator, error_handler)


def main():
    while True:
        user_input = input_parser()
        string = str(get_handler(user_input[0])(user_input[1:]))
        print(string)
        if string == "Good bye!":
            exit()


if __name__ == '__main__':
    main()
