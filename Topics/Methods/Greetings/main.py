class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}!"


n = input()
person = Person(n)
print(person.greet())
