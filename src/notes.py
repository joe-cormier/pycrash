"""
look at pandas and spark on github
"""

# create vehicle from input (user inputs) or from csv file
class StackOverflowUser:

    def __init__(self, name, userid, rep):
        self.name = name
        self.userid = userid
        self.rep = rep

    @classmethod
    def from_input(cls):
        return cls(
            raw_input('Name: '),
            int(raw_input('User ID: ')),
            int(raw_input('Reputation: ')),
        )

"""
use class to set default tire forces to zero to start?
"""

# error if incorrect entry
class Person:

    TITLES = ('Dr', 'Mr', 'Mrs', 'Ms')

    def __init__(self, title, name, surname):
        if title not in self.TITLES:
            raise ValueError("%s is not a valid title." % title)

        self.title = title
        self.name = name
        self.surname = surname

"""
create counter, maybe use to create single time variable?
"""
class InstanceCounter(object):
    count = 0

    def __init__(self, val):
        self.val = val
        InstanceCounter.count += 1

    def set_val(self, newval):
        self.val = newval

    def get_val(self):
        print(self.val)

    def get_count(self):
        print(InstanceCounter.count)

a = InstanceCounter(5)
b = InstanceCounter(10)
c = InstanceCounter(15)

for obj in (a, b, c):
    print("value of obj: %s" % obj.get_val())
    print("Count : %s" % obj.get_count())

"""
static method to ensure correct entry
"""

class MyClass(object):
    count = 0

    def __init__(self, val):
        self.val = self.filterint(val)
        MyClass.count += 1

    @staticmethod
    def filterint(value):
        if not isinstance(value, int):
            print("Entered value is not an INT, value set to 0")
            return 0
        else:
            return value


a = MyClass(5)
b = MyClass(10)
c = MyClass(15)

print(a.val)
print(b.val)
print(c.val)
print(a.filterint(100))


"""
abstract methods inherited
"""
import abc


class My_ABC_Class(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def set_val(self, val):
        return

    @abc.abstractmethod
    def get_val(self):
        return

# Abstract Base Class defined above ^^^

# Custom class inheriting from the above Abstract Base Class, below


class MyClass(My_ABC_Class):

    def set_val(self, input):
        self.val = input

    def get_val(self):
        print("\nCalling the get_val() method")
        print("I'm part of the Abstract Methods defined in My_ABC_Class()")
        return self.val

    def hello(self):
        print("\nCalling the hello() method")
        print("I'm *not* part of the Abstract Methods defined in My_ABC_Class()")

my_class = MyClass()

my_class.set_val(10)
print(my_class.get_val())
my_class.hello()
