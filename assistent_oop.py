from collections import UserDict


class Field:
    def __init__(self, name):
        Field.value = name


class Name(Field):
    pass


class Phone:
    """при спробі наслідування Phone(Field) в обєктах класу Name(Field) при зміні self.phone змінювалося name.value """

    def __init__(self, value):
        self.phone = value


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        if old_phone == new_phone:
            return f'{old_phone} is the same number as {new_phone}'
        else:
            for phone in self.phones:
                if phone.phone == old_phone:
                    self.phones.append(Phone(new_phone))
                    self.phones.pop(self.phones.index(phone))

    def delete_phone(self, delete_phone):
        old_len = len(self.phones)
        for phone in self.phones:
            if phone.phone == delete_phone:
                self.phones.pop(self.phones.index(phone))
                print(f'delete {delete_phone} complete')
        if len(self.phones) == old_len:
            print(f'{delete_phone} not found')


class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record.phones
        else:
            self.data[record.name.value].extend(record.phones)
            set_phones = set(self.data[record.name.value])
            self.data[record.name.value] = list(set_phones)

    def delete_contact(self, name):
        del self.data[name]


""""""
book = AddressBook()
"""Create object AdressBook"""


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
    user_name = ''
    if len(user_input) >= 2:
        for user in book:
            if user_input[0] in [i.phone for i in book[user]]:
                user_name = user
                for phone in book[user]:
                    if phone.phone == user_input[0]:
                        book[user].append(Phone(user_input[1]))
                        book[user].pop(book[user].index(phone))
                        return f"Contact {user_name.title()}: old number {user_input[0]} " \
                               f"successfully changed to {user_input[1]}"
    if not user_name:
        return f"Old number {user_input[0]} not found "


@input_error
def delete_handler(user_input):
    if user_input[0]:
        book.delete_contact(user_input[0])
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
    "phone" - print phone of name: "phone Ivan"
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
def phone_handler(user_input):
    if len(user_input):
        if user_input[0] in book:
            phone_book_list = []
            for phone in book[user_input[0]]:
                phone_book_list.append(f"{user_input[0].title()}: {phone.phone}")
            return "\n".join(phone_book_list)
    else:
        raise KeyError


def show_handler(user_input):
    phone_book_list = []
    for name in book:
        phone_book_list.append(f"{name.title()}: {[i.phone for i in book[name]]}")
    return "\n".join(phone_book_list)


HENDLER_DICT = {
    "add": add_handler,
    "close": exit_handler,
    "change": change_handler,
    "exit": exit_handler,
    "good bye": exit_handler,
    "hello": hello_handler,
    "help": help_hendler,
    "phone": phone_handler,
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
