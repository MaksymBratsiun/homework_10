from collections import UserDict


class Field:
    def __init__(self, name):
        Field.value = name


class Name(Field):
    pass


class Phone(Field):
    pass


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        print('add complete')

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                print('change complete')

    def delete_phone(self, delete_phone):
        for phone in self.phones:
            if phone.value == delete_phone:
                self.phones.remove(phone)
                print('delete complete')


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record.phones

    def delete_contact(self, name):
        del self.data[name]


def main():
    book = AddressBook()
    rec = Record('ivan')
    print(rec.name.value)
    rec.add_phone('+380501234567')
    rec.add_phone('+380671234567')

    print(rec.phones[0])
    book.add_record(rec)
    print(book.data)


if __name__ == '__main__':
    main()
