

class Field:
    def __init__(self, name):
        Field.value = name


class Name(Field):
    pass


class Phone:
    def __init__(self, value):
        self.phone = value


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        print(
            f'For contact {self.name.value} add number {self.phones[-1].phone} to numbers {[i.phone for i in self.phones]}')

    def change_phone(self, old_phone, new_phone):
        if old_phone == new_phone:
            print(f'{old_phone} is the same number as {new_phone}')
        else:
            for phone in self.phones:
                if phone.phone == old_phone:
                    self.phones.append(Phone(new_phone))
                    self.phones.pop(self.phones.index(phone))
                    print(
                        f'For contact {self.name.value} change number {old_phone} to number {new_phone}')

    def delete_phone(self, delete_phone):
        old_len = len(self.phones)
        for phone in self.phones:
            if phone.phone == delete_phone:
                self.phones.pop(self.phones.index(phone))
                print(f'delete {delete_phone} complete')
        if len(self.phones) == old_len:
            print(f'{delete_phone} not found')


rec = Record('ivan')
rec.add_phone('123456789')
rec.add_phone('123456789111')
rec.change_phone('123456789111', '123456789111')
rec.change_phone('123456789111', '123456789112')
rec.delete_phone('111111')
rec.delete_phone('123456789112')
print(f'contact {rec.name.value} - numbers {[i.phone for i in rec.phones]}')
